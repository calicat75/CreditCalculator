from decimal import Decimal
from calculator.app.core.config import settings
from calculator.app.core.logging import get_logger
from calculator.app.models.requests import ScoringDataDto
from calculator.app.models.responses import CreditDto
from calculator.app.utils.calculations import (
    calculate_annuity_payment,
    calculate_psk,
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
            self._validate_scoring(request)

            rate = self._calculate_rate(request)

            amount = self._calculate_amount(request)

            monthly_payment = self._calculate_monthly_payment(
                amount,
                rate,
                request.term,
            )

            payment_schedule = self._generate_schedule(
                amount,
                rate,
                request.term,
                monthly_payment,
            )

            psk = self._calculate_psk(
                amount,
                monthly_payment,
                request.term,
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

        except ValueError:
            logger.warning(
                "Ошибка проверки или расчета кредитной заявки"
            )
            raise

        except Exception:
            logger.exception(
                "Непредвиденная ошибка при расчете кредита"
            )
            raise

    def _validate_scoring(
        self,
        request: ScoringDataDto,
    ) -> None:

        if request.amount <= 0:
            raise ValueError(
                "Сумма кредита должна быть положительной"
            )

        if request.term <= 0:
            raise ValueError(
                "Срок кредита должен быть положительным"
            )

    def _calculate_rate(
        self,
        request: ScoringDataDto,
    ) -> Decimal:

        rate = Decimal(str(settings.base_rate))

        if request.is_insurance_enabled:
            rate -= Decimal(str(settings.insurance_discount))

        if request.is_salary_client:
            rate -= Decimal(str(settings.salary_discount))

        if rate < 0:
            raise ValueError(
                "Процентная ставка не может быть отрицательной"
            )

        return rate

    def _calculate_amount(
        self,
        request: ScoringDataDto,
    ) -> Decimal:

        amount = request.amount

        if request.is_insurance_enabled:
            amount += Decimal(str(settings.insurance_cost))

        return amount

    def _calculate_monthly_payment(
        self,
        amount: Decimal,
        rate: Decimal,
        term: int,
    ) -> Decimal:

        return calculate_annuity_payment(
            amount=amount,
            annual_rate=rate,
            term=term,
        )

    def _generate_schedule(
        self,
        amount: Decimal,
        rate: Decimal,
        term: int,
        monthly_payment: Decimal,
    ):

        return generate_payment_schedule(
            amount=amount,
            annual_rate=rate,
            term=term,
            monthly_payment=monthly_payment,
        )

    def _calculate_psk(
        self,
        amount: Decimal,
        monthly_payment: Decimal,
        term: int,
    ) -> Decimal:

        return calculate_psk(
            amount=amount,
            monthly_payment=monthly_payment,
            term=term,
        )