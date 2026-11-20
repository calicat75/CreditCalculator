from datetime import date
from decimal import Decimal

import pytest

from calculator.app.utils.calculations import (
    add_months,
    calculate_annuity_payment,
    calculate_psk,
    generate_payment_schedule,
    round_money,
)


def test_round_money():
    assert round_money(Decimal("100.125")) == Decimal("100.13")
    assert round_money(Decimal("100.124")) == Decimal("100.12")


def test_calculate_annuity_payment():
    payment = calculate_annuity_payment(
        amount=Decimal("300000"),
        annual_rate=Decimal("12"),
        term=12,
    )

    assert payment == Decimal("26654.70")


def test_calculate_annuity_payment_with_zero_rate():
    payment = calculate_annuity_payment(
        amount=Decimal("120000"),
        annual_rate=Decimal("0"),
        term=12,
    )

    assert payment == Decimal("10000.00")


@pytest.mark.parametrize(
    ("amount", "annual_rate", "term"),
    [
        (Decimal("0"), Decimal("12"), 12),
        (Decimal("-1000"), Decimal("12"), 12),
        (Decimal("1000"), Decimal("12"), 0),
        (Decimal("1000"), Decimal("-1"), 12),
    ],
)
def test_calculate_annuity_payment_invalid_data(
    amount,
    annual_rate,
    term,
):
    with pytest.raises(ValueError):
        calculate_annuity_payment(
            amount,
            annual_rate,
            term,
        )


def test_add_months():
    assert add_months(
        date(2026, 1, 31),
        1,
    ) == date(2026, 2, 28)

    assert add_months(
        date(2026, 1, 15),
        2,
    ) == date(2026, 3, 15)


def test_generate_payment_schedule():
    amount = Decimal("120000")
    rate = Decimal("12")
    term = 12

    monthly_payment = calculate_annuity_payment(
        amount,
        rate,
        term,
    )

    schedule = generate_payment_schedule(
        amount=amount,
        annual_rate=rate,
        term=term,
        monthly_payment=monthly_payment,
        start_date=date(2026, 1, 15),
    )

    assert len(schedule) == term
    assert schedule[0].number == 1
    assert schedule[0].date == date(2026, 2, 15)
    assert schedule[-1].number == 12
    assert schedule[-1].remaining_debt == Decimal("0.00")


def test_schedule_has_correct_payment_parts():
    schedule = generate_payment_schedule(
        amount=Decimal("120000"),
        annual_rate=Decimal("12"),
        term=12,
        monthly_payment=Decimal("10661.85"),
        start_date=date(2026, 1, 15),
    )

    first_payment = schedule[0]

    assert first_payment.total_payment == (
        first_payment.interest_payment
        + first_payment.debt_payment
    )


def test_calculate_psk():
    psk = calculate_psk(
        amount=Decimal("120000"),
        monthly_payment=Decimal("10661.85"),
        term=12,
    )

    assert psk > Decimal("0")


def test_calculate_psk_without_overpayment():
    psk = calculate_psk(
        amount=Decimal("120000"),
        monthly_payment=Decimal("10000"),
        term=12,
    )

    assert psk == Decimal("0.00")


@pytest.mark.parametrize(
    ("amount", "monthly_payment", "term"),
    [
        (Decimal("0"), Decimal("10000"), 12),
        (Decimal("100000"), Decimal("0"), 12),
        (Decimal("100000"), Decimal("10000"), 0),
    ],
)
def test_calculate_psk_invalid_data(
    amount,
    monthly_payment,
    term,
):
    with pytest.raises(ValueError):
        calculate_psk(
            amount,
            monthly_payment,
            term,
        )