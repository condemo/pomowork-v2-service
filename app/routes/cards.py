from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.oauth2 import get_current_user
from app.models.cards import CardModel
from app.models.projects import ProjectModel
from app.schemas.cards import CardResponse, CardCreate, CardUpdate


router = APIRouter(
    prefix="/cards",
    tags=["Cards"],
)


@router.get("/", response_model=list[CardResponse])
async def get_all_cards(db: Session = Depends(get_db),
                        current_user: str = Depends(get_current_user)):
    card_list = db.query(CardModel) \
        .join(ProjectModel, ProjectModel.owner_id == current_user.id) \
        .filter(ProjectModel.id == CardModel.project_id) \
        .all()

    return card_list


@router.get("/{projectid}", response_model=list[CardResponse])
async def get_project_card(projectid: int, db: Session = Depends(get_db),
                           current_user: str = Depends(get_current_user)):
    project = db.query(ProjectModel).filter(ProjectModel.id == projectid).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The project with id {projectid} is not found",
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorize to perform requested action",
        )
    card_list = db.query(CardModel).filter(CardModel.project_id == projectid).all()

    return card_list


@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def create_card(card: CardCreate, db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user)):
    project = db.query(ProjectModel).filter(ProjectModel.id == card.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The project with id {card.project_id} is not found ",
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorize to perform requested action",
        )

    new_card = CardModel(**card.dict())
    db.add(new_card)
    db.commit()
    db.refresh(new_card)

    return new_card


@router.delete("/{project_id}/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(project_id: int, id: int, db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()

    query = db.query(CardModel).filter(CardModel.id == id)
    card = query.first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The project with id {project_id} is not found",
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorize to perform requested action",
        )
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The card with id {id} is not found"
        )

    query.delete(synchronize_session=False)
    db.commit()

    return


@router.put("/{project_id}/{id}", response_model=CardResponse)
async def update_card(project_id: int, id: int,
                      updated_card: CardUpdate, db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()

    query = db.query(CardModel).filter(CardModel.id == updated_card.id)
    card = query.first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The project with id {project_id} is not found",
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorize to perform requested action",
        )
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The card with id {updated_card.id} is not found"
        )

    query.update(updated_card.dict(), synchronize_session=False)
    db.commit()

    return query.first()
