from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from models.company import Company

from crud.company import (
    create_company,
    delete_company,
    get_companies,
    get_company,
    update_company,
)
from database import SessionLocal
from schemas.company import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
)
from utils.jwt import get_current_user
from models.company import Company   # ★ admin/all で必要

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

auth_scheme = HTTPBearer()   # ★ OAuth2 を完全に削除して JWT に統一


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_user(token = Depends(auth_scheme)):
    # token.credentials に JWT が入っている
    user = get_current_user(token.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


@router.get("/", response_model=list[CompanyResponse])
def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    return get_companies(db, user.id, skip, limit)


@router.get("/{company_id}", response_model=CompanyResponse)
def read_company(
    company_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    company = get_company(db, company_id, user.id)

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


@router.post("/", response_model=CompanyResponse, status_code=201)
def create(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    return create_company(db, company, user.id)


@router.put("/{company_id}", response_model=CompanyResponse)
def update(
    company_id: UUID,
    company: CompanyUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    updated = update_company(db, company_id, company, user.id)

    if updated is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return updated


@router.delete("/{company_id}", status_code=204)
def delete(
    company_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    success = delete_company(db, company_id, user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Company not found")

    return


@router.get("/admin/all", response_model=list[CompanyResponse])
def read_all_companies(
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return db.query(Company).all()
