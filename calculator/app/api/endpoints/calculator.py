from fastapi import APIRouter, HTTPException

from app.models.requests import (
    LoanStatementRequestDto,
    ScoringDataDto,
)
from app.models.responses import (
    CreditDto,
    LoanOfferDto,
)
from app.services.credit_service import CreditService
from app.services.offer_service import OfferService


router = APIRouter(
    prefix="/calculator",
    tags=["Calculator"],
)

offer_service = OfferService()
credit_service = CreditService()


@router.post(
    "/offers",
    response_model=list[LoanOfferDto],
    summary="Получение кредитных предложений",
)
def get_loan_offers(
    request: LoanStatementRequestDto,
) -> list[LoanOfferDto]:
    try:
        return offer_service.calculate_offers(request)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.post(
    "/calc",
    response_model=CreditDto,
    summary="Полный расчет кредита",
)
def calculate_credit(
    request: ScoringDataDto,
) -> CreditDto:
    try:
        return credit_service.calculate_credit(request)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error