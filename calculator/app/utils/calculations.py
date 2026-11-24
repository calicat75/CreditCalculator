from calendar import monthrange
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from app.core.exceptions import CalculationError
from app.models.responses import PaymentScheduleElementDto


CENT = Decimal("0.01")
ONE = Decimal("1")


def round_money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_annuity_payment(
    amount: Decimal,
    annual_rate: Decimal,
    term: int,
) -> Decimal:
    """Рассчитывает ежемесячный аннуитетный платеж."""

    monthly_rate = annual_rate / Decimal("1200")

    if monthly_rate == 0:
        return round_money(amount / Decimal(term))

    factor = (ONE + monthly_rate) ** term

    return round_money(
        amount * monthly_rate * factor / (factor - ONE)
    )


def calculate_rate(
    base_rate: Decimal,
    insurance: bool,
    salary: bool,
    insurance_discount: Decimal,
    salary_discount: Decimal,
) -> Decimal:
    """Рассчитывает процентную ставку с учетом скидок."""

    rate = base_rate

    if insurance:
        rate -= insurance_discount

    if salary:
        rate -= salary_discount

    if rate < 0:
        raise CalculationError("Процентная ставка не может быть отрицательной")

    return rate


def calculate_total_amount(
    amount: Decimal,
    insurance: bool,
    insurance_cost: Decimal,
) -> Decimal:
    """Рассчитывает полную сумму кредита с учетом стоимости страховки."""

    if insurance:
        return amount + insurance_cost

    return amount


def add_months(source_date: date, months: int) -> date:
    month_index = source_date.month - 1 + months

    year = source_date.year + month_index // 12
    month = month_index % 12 + 1

    last_day = monthrange(year, month)[1]

    return date(year, month, min(source_date.day, last_day))


def generate_payment_schedule(
    amount: Decimal,
    annual_rate: Decimal,
    term: int,
    monthly_payment: Decimal,
    start_date: date | None = None,
) -> list[PaymentScheduleElementDto]:
    """Генерирует график ежемесячных платежей."""

    if start_date is None:
        start_date = date.today()

    monthly_rate = annual_rate / Decimal("1200")
    remaining_debt = round_money(amount)

    schedule = []

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
                raise CalculationError(
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


def calculate_psk(
    amount: Decimal,
    monthly_payment: Decimal,
    term: int,
) -> Decimal:
    """Рассчитывает эффективную годовую ставку по ежемесячным платежам."""

    low = Decimal("0")
    high = Decimal("1")

    for _ in range(200):
        monthly_rate = (low + high) / Decimal("2")

        if monthly_rate == 0:
            calculated_amount = monthly_payment * term
        else:
            factor = (ONE + monthly_rate) ** term

            calculated_amount = (
                monthly_payment
                * (factor - ONE)
                / (monthly_rate * factor)
            )

        if calculated_amount > amount:
            low = monthly_rate
        else:
            high = monthly_rate

    monthly_rate = (low + high) / Decimal("2")

    annual_rate = (
        (ONE + monthly_rate) ** 12 - ONE
    ) * Decimal("100")

    return round_money(annual_rate)