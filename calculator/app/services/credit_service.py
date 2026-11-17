from calculator.app.models.requests import ScoringDataDto
from calculator.app.models.responses import CreditDto


class CreditService:

    def calculate_credit(
        self,
        request: ScoringDataDto,
    ) -> CreditDto:

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
            payment_schedule,
            amount,
        )

        return CreditDto(
            amount=amount,
            term=request.term,
            monthlyPayment=monthly_payment,
            rate=rate,
            psk=psk,
            isInsuranceEnabled=request.is_insurance_enabled,
            isSalaryClient=request.is_salary_client,
            paymentSchedule=payment_schedule,
        )