from decimal import Decimal

from app.core.config import settings
from app.core.exceptions import CalculationError
from app.core.logging import get_logger
from app.models.requests import ScoringDataDto
from app.models.responses import CreditDto
from app.utils.calculations import (
    calculate_annuity_payment,
    calculate_psk,
    calculate_rate,
    calculate_total_amount,
    generate_payment_schedule,
)

logger = get_logger(__name__)


class CreditService:

    def calculate_credit(
        self,
        request: ScoringDataDto,
    ) -> CreditDto:
        logger.info(
            "Начат расчет кредита: amount=%s, term=%s",
            request.amount,
            request.term,
        )

        try:
            rate = calculate_rate(
                base_rate=Decimal(str(settings.base_rate)),
                insurance=request.is_insurance_enabled,
                salary=request.is_salary_client,
                insurance_discount=Decimal(str(settings.insurance_discount)),
                salary_discount=Decimal(str(settings.salary_discount)),
            )

            amount = calculate_total_amount(
                amount=request.amount,
                insurance=request.is_insurance_enabled,
                insurance_cost=Decimal(str(settings.insurance_cost)),
            )

            monthly_payment = calculate_annuity_payment(
                amount=amount,
                annual_rate=rate,
                term=request.term,
            )

            payment_schedule = generate_payment_schedule(
                amount=amount,
                annual_rate=rate,
                term=request.term,
                monthly_payment=monthly_payment,
            )

            psk = calculate_psk(
                amount=amount,
                monthly_payment=monthly_payment,
                term=request.term,
            )

            credit = CreditDto(
                amount=amount,
                term=request.term,
                monthlyPayment=monthly_payment,
                rate=rate,
                psk=psk,
                isInsuranceEnabled=request.is_insurance_enabled,
                isSalaryClient=request.is_salary_client,
                paymentSchedule=payment_schedule,
            )

            logger.info(
                "Расчет кредита завершен: amount=%s, rate=%s, psk=%s",
                credit.amount,
                credit.rate,
                credit.psk,
            )

            return credit

        except CalculationError:
            logger.warning(
                "Ошибка расчета кредитной заявки"
            )
            raise

        except Exception:
            logger.exception(
                "Непредвиденная ошибка при расчете кредита"
            )
            raise
