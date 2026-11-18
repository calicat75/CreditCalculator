from calendar import monthrange
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from app.models.responses import PaymentScheduleElementDto

CENT = Decimal("0.01")
ONE = Decimal("1")
TWELVE = Decimal("12")

def round_money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_annuity_payment(
    amount: Decimal,            #сумма кредита
    annual_rate: Decimal,       #годовая процентная ставка в процентах
    term: int,                  #срок кредита в месяцах
) -> Decimal:

    if amount <= 0:
        raise ValueError("Сумма кредита должна быть положительной")

    if term <= 0:
        raise ValueError("Срок кредита должен быть положительным")

    if annual_rate < 0:
        raise ValueError("Процентная ставка не может быть отрицательной")

    monthly_rate = annual_rate / Decimal("1200")

    if monthly_rate == 0:
        return round_money(amount / Decimal(term))

    coefficient = (
        monthly_rate
        * (ONE + monthly_rate) ** term
        / ((ONE + monthly_rate) ** term - ONE)
    )

    return round_money(amount * coefficient)


def add_months(source_date: date, months: int) -> date:
    month_index = source_date.month - 1 + months

    year = source_date.year + month_index // 12
    month = month_index % 12 + 1

    last_day = monthrange(year, month)[1]
    day = min(source_date.day, last_day)

    return date(year, month, day)

#помесячный график погашения кредита
def generate_payment_schedule(
    amount: Decimal,
    annual_rate: Decimal,
    term: int,
    monthly_payment: Decimal,
    start_date: date | None = None,
) -> list[PaymentScheduleElementDto]:

    if amount <= 0:
        raise ValueError("Сумма кредита должна быть положительной")

    if term <= 0:
        raise ValueError("Срок кредита должен быть положительным")

    if annual_rate < 0:
        raise ValueError("Процентная ставка не может быть отрицательной")

    if monthly_payment <= 0:
        raise ValueError("Ежемесячный платеж должен быть положительным")

    if start_date is None:
        start_date = date.today()

    monthly_rate = annual_rate / Decimal("1200")
    remaining_debt = round_money(amount)

    schedule: list[PaymentScheduleElementDto] = []

    for number in range(1, term + 1):
        interest_payment = round_money(
            remaining_debt * monthly_rate
        )

        if number == term:
            debt_payment = remaining_debt
            total_payment = round_money(
                debt_payment + interest_payment
            )
        else:
            total_payment = monthly_payment
            debt_payment = round_money(
                total_payment - interest_payment
            )

            if debt_payment <= 0:
                raise ValueError(
                    "Ежемесячный платеж недостаточен для погашения долга"
                )

            if debt_payment > remaining_debt:
                debt_payment = remaining_debt
                total_payment = round_money(
                    debt_payment + interest_payment
                )

        remaining_debt = round_money(
            remaining_debt - debt_payment
        )

        if remaining_debt < 0:
            remaining_debt = Decimal("0.00")

        schedule.append(
            PaymentScheduleElementDto(
                number=number,
                date=add_months(start_date, number),
                totalPayment=total_payment,
                interestPayment=interest_payment,
                debtPayment=debt_payment,
                remainingDebt=remaining_debt,
            )
        )

    return schedule