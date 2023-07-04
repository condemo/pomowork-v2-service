from app.dependencies.oauth2 import get_current_user
from app.schemas.projects import ProjectUpdate
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models import ProjectModel
from app.schemas.projects import ProjectResponse, ProjectCreate

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("/", response_model=list[ProjectResponse])
async def get_all_projects(db: Session = Depends(get_db),
                           current_user: int = Depends(get_current_user)):
    projects_list = db.query(ProjectModel).all()

    return projects_list


@router.get("/{id}", response_model=ProjectResponse)
async def get_one_project(id: int, db: Session = Depends(get_db),
                          current_user: int = Depends(get_current_user)):
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()

    return project


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=ProjectResponse)
async def create_project(project: ProjectCreate,
                         db: Session = Depends(get_db),
                         current_user: int = Depends(get_current_user)):
    new_project = ProjectModel(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(id: int, db: Session = Depends(get_db),
                         current_user: int = Depends(get_current_user)):
    query = db.query(ProjectModel).filter(ProjectModel.id == id)

    query.delete(synchronize_session=False)
    db.commit()

    return


@router.put("/", response_model=ProjectResponse)
async def update_project(project: ProjectUpdate, db: Session = Depends(get_db),
                         current_user: int = Depends(get_current_user)):
    query = db.query(ProjectModel).filter(ProjectModel.id == project.id)
    # TODO: Descomentar para gestionar errores
    # project_updated = query.first()

    query.update(project.dict(), synchronize_session=False)
    db.commit()

    return query.first()
