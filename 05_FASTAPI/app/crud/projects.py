from sqlalchemy.orm import Session
from uuid import UUID

from models.projects import Project
from schemas.projects import ProjectCreate


# Create
def create_project(db: Session, project: ProjectCreate):
    db_project = Project(
        project_name=project.project_name,
        project_type=project.project_type,
        budget=project.budget,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        status=project.status,
        company_id=project.company_id,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


# Read all
def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()


# Read one
def get_project(db: Session, project_id: UUID):
    return db.query(Project).filter(Project.id == project_id).first()


# Read by company
def get_projects_by_company(db: Session, company_id: UUID):
    return db.query(Project).filter(Project.company_id == company_id).all()


# Update
def update_project(db: Session, project_id: UUID, project: ProjectCreate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        return None

    db_project.project_name = project.project_name
    db_project.project_type = project.project_type
    db_project.budget = project.budget
    db_project.description = project.description
    db_project.start_date = project.start_date
    db_project.end_date = project.end_date
    db_project.status = project.status
    db_project.company_id = project.company_id

    db.commit()
    db.refresh(db_project)
    return db_project


# Delete
def delete_project(db: Session, project_id: UUID):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        return None

    db.delete(db_project)
    db.commit()
    return db_project
