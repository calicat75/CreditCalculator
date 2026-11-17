from decimal import Decimal
from itertools import product
from uuid import uuid4

from calculator.app.core.config import settings
from calculator.app.models.requests import LoanStatementRequestDto
from calculator.app.models.responses import LoanOfferDto


class OfferService:

    def calculate_offers(
        self,
        request: LoanStatementRequestDto,
    ) -> list[LoanOfferDto]:

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

        return sorted(
            offers,
            key=lambda offer: offer.rate,
            reverse=True,
        )

    def _prescore(self, request):
        #TODO: логика проверки
        pass

    def _calculate_rate(self, insurance, salary):
        rate = Decimal(str(settings.base_rate))

        if insurance:
            rate -= Decimal(str(settings.insurance_discount))

        if salary:
            rate -= Decimal(str(settings.salary_discount))

        return rate

    def _calculate_total_amount(self, amount, insurance):
        total = amount

        if insurance:
            total += Decimal(str(settings.insurance_cost))

        return total

    def _calculate_monthly_payment(
        self,
        amount,
        rate,
        term,
    ):# вынести формулу чуть позже
        pass