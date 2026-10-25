from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.projects import Project, ProjectCreate
from crud import projects as crud_projects
from utils.jwt import get_current_user_from_token

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

auth_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    return get_current_user_from_token(credentials.credentials)

# 全件取得
@router.get("/", response_model=list[Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    return crud_projects.get_projects(db, skip=skip, limit=limit)


# 1件取得
@router.get("/{project_id}", response_model=Project)
def read_project(project_id: UUID, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    db_project = crud_projects.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


# 企業別の案件一覧
@router.get("/company/{company_id}", response_model=list[Project])
def read_projects_by_company(company_id: UUID, db: Session = Depends(get_db),
                            current_user: dict = Depends(get_current_user)):
    return crud_projects.get_projects_by_company(db, company_id)


# 作成
@router.post("/", response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    return crud_projects.create_project(db, project)


# 更新
@router.put("/{project_id}", response_model=Project)
def update_project(project_id: UUID, project: ProjectCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    db_project = crud_projects.update_project(db, project_id, project)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


# 削除
@router.delete("/{project_id}")
def delete_project(project_id: UUID, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    db_project = crud_projects.delete_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted"}
