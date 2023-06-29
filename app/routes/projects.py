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
async def get_all_projects(db: Session = Depends(get_db)):
    projects_list = db.query(ProjectModel).all()

    return projects_list


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=ProjectResponse)
async def create_project(project: ProjectCreate,
                         db: Session = Depends(get_db)):
    new_project = ProjectModel(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    print(new_project.id)

    return new_project
