from decimal import Decimal
from itertools import product
from uuid import uuid4

from app.core.config import settings
from app.core.exceptions import CalculationError
from app.core.logging import get_logger
from app.models.requests import LoanStatementRequestDto
from app.models.responses import LoanOfferDto
from app.utils.calculations import (
    calculate_annuity_payment,
    calculate_rate,
    calculate_total_amount,
)

logger = get_logger(__name__)


class OfferService:

    def calculate_offers(
        self,
        request: LoanStatementRequestDto,
    ) -> list[LoanOfferDto]:
        logger.info(
            "Начат расчет кредитных предложений: amount=%s, term=%s",
            request.amount,
            request.term,
        )

        try:
            statement_id = uuid4()
            offers = []

            for insurance, salary in product(
                [False, True],
                repeat=2,
            ):
                rate = calculate_rate(
                    base_rate=Decimal(str(settings.base_rate)),
                    insurance=insurance,
                    salary=salary,
                    insurance_discount=Decimal(str(settings.insurance_discount)),
                    salary_discount=Decimal(str(settings.salary_discount)),
                )

                total_amount = calculate_total_amount(
                    amount=request.amount,
                    insurance=insurance,
                    insurance_cost=Decimal(str(settings.insurance_cost)),
                )

                monthly_payment = calculate_annuity_payment(
                    amount=total_amount,
                    annual_rate=rate,
                    term=request.term,
                )

                offers.append(
                    LoanOfferDto(
                        statementId=statement_id,
                        requestedAmount=request.amount,
                        totalAmount=total_amount,
                        term=request.term,
                        monthlyPayment=monthly_payment,
                        rate=rate,
                        isInsuranceEnabled=insurance,
                        isSalaryClient=salary,
                    )
                )

            offers = sorted(
                offers,
                key=lambda offer: offer.rate,
                reverse=True,
            )

            logger.info(
                "Расчет кредитных предложений завершен: offers_count=%s",
                len(offers),
            )

            return offers

        except CalculationError:
            logger.warning(
                "Ошибка расчета кредитных предложений"
            )
            raise

        except Exception:
            logger.exception(
                "Непредвиденная ошибка при расчете кредитных предложений"
            )
            raise
