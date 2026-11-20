from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LoanOfferDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    statement_id: UUID = Field(alias="statementId")

    requested_amount: Decimal = Field(alias="requestedAmount")
    total_amount: Decimal = Field(alias="totalAmount")

    term: int

    monthly_payment: Decimal = Field(alias="monthlyPayment")
    rate: Decimal

    is_insurance_enabled: bool = Field(
        alias="isInsuranceEnabled"
    )
    is_salary_client: bool = Field(
        alias="isSalaryClient"
    )


class PaymentScheduleElementDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    number: int
    date: date

    total_payment: Decimal = Field(alias="totalPayment")
    interest_payment: Decimal = Field(alias="interestPayment")
    debt_payment: Decimal = Field(alias="debtPayment")
    remaining_debt: Decimal = Field(alias="remainingDebt")


class CreditDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    amount: Decimal
    term: int

    monthly_payment: Decimal = Field(alias="monthlyPayment")
    rate: Decimal
    psk: Decimal

    is_insurance_enabled: bool = Field(
        alias="isInsuranceEnabled"
    )
    is_salary_client: bool = Field(
        alias="isSalaryClient"
    )

    payment_schedule: list[PaymentScheduleElementDto] = Field(
        alias="paymentSchedule"
    )