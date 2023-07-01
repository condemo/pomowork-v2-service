from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.cards import CardModel
from app.schemas.cards import CardResponse, CardCreate, CardUpdate


router = APIRouter(
    prefix="/cards",
    tags=["Cards"],
)


@router.get("/", response_model=list[CardResponse])
async def get_all_cards(db: Session = Depends(get_db)):
    card_list = db.query(CardModel).all()

    return card_list


@router.get("/{projectid}", response_model=list[CardResponse])
async def get_project_card(projectid: int, db: Session = Depends(get_db)):
    card_list = db.query(CardModel).filter(CardModel.project_id == projectid).all()

    return card_list


@router.post("/", response_model=CardResponse)
async def create_card(card: CardCreate, db: Session = Depends(get_db)):
    new_card = CardModel(**card.dict())
    db.add(new_card)
    db.commit()
    db.refresh(new_card)

    return new_card


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(id: int, db: Session = Depends(get_db)):
    query = db.query(CardModel).filter(CardModel.id == id)
    # TODO: Descomentar para implementar sistema de errores
    # card = query.first()

    query.delete(synchronize_session=False)
    db.commit()

    return


@router.put("/", response_model=CardResponse)
async def update_card(card: CardUpdate, db: Session = Depends(get_db)):
    query = db.query(CardModel).filter(CardModel.id == card.id)
    # TODO: Descomentar para implementar sistema de errores
    # updated_card = query.first()

    query.update(card.dict(), synchronize_session=False)
    db.commit()

    return query.first()
