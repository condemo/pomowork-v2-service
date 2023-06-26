from fastapi import APIRouter


router = APIRouter(
    prefix="/cards",
    tags=["Cards"],
)


@router.get("/")
async def root():
    return {"message": "Cards Route"}
