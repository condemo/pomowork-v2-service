from fastapi import APIRouter


router = APIRouter(
    prefix="/extras",
    tags=["Extras"],
)


@router.get("/")
async def root():
    return {"message": "Extras Route"}
