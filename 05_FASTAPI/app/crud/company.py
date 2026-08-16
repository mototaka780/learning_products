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
        website=company.website,
        notes=company.notes,
        user_id=user_id  # ★ 追加
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def get_company(db: Session, company_id: UUID, user_id: UUID):
    return db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == user_id  # ★ 自分の会社だけ取得
    ).first()


def get_companies(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return db.query(Company).filter(
        Company.user_id == user_id  # ★ 自分の会社だけ一覧取得
    ).offset(skip).limit(limit).all()


def update_company(db: Session, company_id: UUID, company: CompanyUpdate, user_id: UUID):
    db_company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == user_id  # ★ 自分の会社だけ更新可能
    ).first()

    if not db_company:
        return None

    for key, value in company.model_dump(exclude_unset=True).items():
        setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: UUID, user_id: UUID):
    db_company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == user_id  # ★ 自分の会社だけ削除可能
    ).first()

    if not db_company:
        return None

    db.delete(db_company)
    db.commit()
    return True
