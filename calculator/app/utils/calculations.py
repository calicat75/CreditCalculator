from decimal import Decimal, ROUND_HALF_UP


def round_money(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def calculate_annuity_payment(
    amount: Decimal,
    annual_rate: Decimal,
    term: int,
) -> Decimal:

    if amount <= 0 or term <= 0:
        raise ValueError("Amount and term must be positive")

    if annual_rate < 0:
        raise ValueError("Rate cannot be negative")

    monthly_rate = annual_rate / Decimal("1200")

    if monthly_rate == 0:
        return round_money(amount / term)

    coefficient = (
        monthly_rate
        * (1 + monthly_rate) ** term
        / ((1 + monthly_rate) ** term - 1)
    )

    return round_money(amount * coefficient)