from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import cards, projects


app = FastAPI(
    title="PomoWork",
    description="Una app para controlar pomodoros y cobros en distintos proyectos",
)

origins = [
    # TODO: Configurar bien antes del deploy
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cards.router)
app.include_router(projects.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
