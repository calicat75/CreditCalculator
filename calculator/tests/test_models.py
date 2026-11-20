import pytest
from pydantic import ValidationError

from calculator.app.models.requests import LoanStatementRequestDto


def test_valid_loan_statement():
    data = {
        "amount": "500000",
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan@example.com",
        "birthdate": "1995-05-15",
        "passportSeries": "1234",
        "passportNumber": "123456",
    }

    model = LoanStatementRequestDto(**data)

    assert model.amount == 500000
    assert model.term == 12


def test_negative_amount_is_invalid():
    data = {
        "amount": "-1000",
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan@example.com",
        "birthdate": "1995-05-15",
        "passportSeries": "1234",
        "passportNumber": "123456",
    }

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**data)