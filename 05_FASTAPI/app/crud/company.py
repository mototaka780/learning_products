from uuid import UUID
from sqlalchemy.orm import Session
from models.company import Company
from schemas.company import CompanyCreate, CompanyUpdate


def create_company(db: Session, company: CompanyCreate, user_id: UUID):
    new_company = Company(
        company_name=company.company_name,
        industry=company.industry,
        city=company.city,
        country=company.country,
        employee_count=company.employee_count,
        website=str(company.website),
        notes=company.notes,
        user_id=user_id
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def get_company(db: Session, company_id: UUID, user_id: UUID):
    return db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == user_id
    ).first()


def get_companies(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return db.query(Company).filter(
        Company.user_id == user_id
    ).offset(skip).limit(limit).all()


def update_company(db: Session, company_id: UUID, company: CompanyUpdate, user_id: UUID):
    db_company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == user_id
    ).first()

    if not db_company:
        return None

    update_data = company.model_dump(exclude_unset=True)

    # HttpUrl → str
    if update_data.get("website") is not None:
        update_data["website"] = str(update_data["website"])

    for key, value in update_data.items():
        setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: UUID, user_id: UUID):
    db_company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == user_id
    ).first()

    if not db_company:
        return None

    db.delete(db_company)
    db.commit()
    return True