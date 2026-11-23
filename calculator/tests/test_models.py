import pytest
from pydantic import ValidationError

from app.models.requests import LoanStatementRequestDto


@pytest.fixture
def valid_loan_data():
    return {
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


def test_valid_loan_statement(valid_loan_data):
    model = LoanStatementRequestDto(**valid_loan_data)

    assert model.amount == 500000
    assert model.term == 12


def test_negative_amount_is_invalid(valid_loan_data):
    valid_loan_data["amount"] = "-1000"

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)


def test_amount_below_minimum_is_invalid(valid_loan_data):
    valid_loan_data["amount"] = "9999"

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)


def test_amount_above_maximum_is_invalid(valid_loan_data):
    valid_loan_data["amount"] = "5000001"

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)


def test_term_below_minimum_is_invalid(valid_loan_data):
    valid_loan_data["term"] = 5

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)


def test_term_above_maximum_is_invalid(valid_loan_data):
    valid_loan_data["term"] = 61

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)


@pytest.mark.parametrize(
    "field",
    ["firstName", "lastName", "middleName"],
)
@pytest.mark.parametrize(
    "value",
    ["Ivan1", "I", "Ivan!", "12345"],
)
def test_invalid_name_is_rejected(valid_loan_data, field, value):
    valid_loan_data[field] = value

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)


def test_invalid_passport_series_is_rejected(valid_loan_data):
    valid_loan_data["passportSeries"] = "123"

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)


def test_invalid_passport_number_is_rejected(valid_loan_data):
    valid_loan_data["passportNumber"] = "12345"

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)


@pytest.mark.parametrize(
    "birthdate",
    [
        "2010-01-01",
        "1950-01-01",
    ],
)
def test_invalid_age_is_rejected(valid_loan_data, birthdate):
    valid_loan_data["birthdate"] = birthdate

    with pytest.raises(ValidationError):
        LoanStatementRequestDto(**valid_loan_data)