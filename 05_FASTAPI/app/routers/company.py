from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.company import Company

from crud.company import (
    create_company,
    delete_company,
    get_companies,
    get_company,
    update_company,
)

from database import get_db

from schemas.company import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
)

from routers.auth import get_current_user


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# =========================================================
# 会社一覧取得
# =========================================================
@router.get(
    "/",
    response_model=list[CompanyResponse]
)
def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_companies(
        db,
        user.id,
        skip,
        limit
    )


# =========================================================
# 会社取得
# =========================================================
@router.get(
    "/{company_id}",
    response_model=CompanyResponse
)
def read_company(
    company_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    company = get_company(
        db,
        company_id,
        user.id
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


# =========================================================
# 会社登録
# =========================================================
@router.post(
    "/",
    response_model=CompanyResponse,
    status_code=201
)
def create(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_company(
        db,
        company,
        user.id
    )


# =========================================================
# 会社更新
# =========================================================
@router.put(
    "/{company_id}",
    response_model=CompanyResponse
)
def update(
    company_id: UUID,
    company: CompanyUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    updated = update_company(
        db,
        company_id,
        company,
        user.id
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return updated


# =========================================================
# 会社削除
# =========================================================
@router.delete(
    "/{company_id}",
    status_code=204
)
def delete(
    company_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    success = delete_company(
        db,
        company_id,
        user.id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return


# =========================================================
# 管理者：全会社取得
# =========================================================
@router.get(
    "/admin/all",
    response_model=list[CompanyResponse]
)
def read_all_companies(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return db.query(Company).all()

