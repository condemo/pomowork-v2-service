from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.routes import cards, projects, users, login
from app.dependencies.oauth2 import get_current_user


app = FastAPI(
    title="PomoWork",
    description="Una app para controlar pomodoros y cobros en distintos proyectos",
    version="alpha-0.0.1",
    contact={
        "name": "Gustavo de los Santos",
        "email": "gusleo94@gmail.com"
    },
    license_info={
        "name": "MIT",
    }
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
app.include_router(users.router)
app.include_router(login.router)


@app.get("/")
async def root(current_user: int = Depends(get_current_user)):
    return {"message": "OK"}
