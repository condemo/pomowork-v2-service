FROM ubuntu:latest AS builder-image

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt install --no-install-recommends -y \
  python3.10 python3.10-dev python3-pip python3.10-venv python3-wheel \
  build-essential && apt clean  && rm -rf /var/lib/apt/lists/*

RUN python3.10 -m venv /home/gus/venv
ENV PATH="/home/gus/venv/bin:$PATH"

COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu:latest AS runner-image
RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3-venv && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home gus
COPY --from=builder-image /home/gus/venv /home/gus/venv

USER gus
RUN mkdir /home/gus/code
WORKDIR /home/gus/code

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/home/gus/venv
ENV PATH="/home/gus/venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
