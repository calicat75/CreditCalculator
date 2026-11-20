from decimal import Decimal
from itertools import product
from uuid import uuid4
from calculator.app.core.config import settings
from calculator.app.core.logging import get_logger
from calculator.app.models.requests import LoanStatementRequestDto
from calculator.app.models.responses import LoanOfferDto
from calculator.app.utils.calculations import calculate_annuity_payment

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
            self._prescore(request)

            statement_id = uuid4()
            offers = []

            for insurance, salary in product(
                [False, True],
                repeat=2,
            ):
                rate = self._calculate_rate(
                    insurance,
                    salary,
                )

                total_amount = self._calculate_total_amount(
                    request.amount,
                    insurance,
                )

                monthly_payment = self._calculate_monthly_payment(
                    total_amount,
                    rate,
                    request.term,
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

        except ValueError:
            logger.warning(
                "Ошибка проверки кредитной заявки"
            )
            raise

        except Exception:
            logger.exception(
                "Непредвиденная ошибка при расчете кредитных предложений"
            )
            raise

    def _prescore(
        self,
        request: LoanStatementRequestDto,
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
        insurance: bool,
        salary: bool,
    ) -> Decimal:

        rate = Decimal(str(settings.base_rate))

        if insurance:
            rate -= Decimal(str(settings.insurance_discount))

        if salary:
            rate -= Decimal(str(settings.salary_discount))

        if rate < 0:
            raise ValueError(
                "Процентная ставка не может быть отрицательной"
            )

        return rate

    def _calculate_total_amount(
        self,
        amount: Decimal,
        insurance: bool,
    ) -> Decimal:
        total = amount
        if insurance:
            total += Decimal(str(settings.insurance_cost))
        return total

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