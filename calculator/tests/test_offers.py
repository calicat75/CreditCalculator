from decimal import Decimal
from uuid import UUID
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def loan_request():
    return {
        "amount": 300000,
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan@example.com",
        "birthdate": "1995-05-15",
        "passportSeries": "1234",
        "passportNumber": "567890",
    }


def test_get_loan_offers_returns_four_offers(loan_request):

    response = client.post("/calculator/offers", json=loan_request)

    assert response.status_code == 200
    offers = response.json()
    assert isinstance(offers, list)
    assert len(offers) == 4


def test_loan_offers_have_correct_fields(loan_request):

    response = client.post("/calculator/offers", json=loan_request)
    assert response.status_code == 200
    offers = response.json()

    expected_fields = {
        "statementId",
        "requestedAmount",
        "totalAmount",
        "term",
        "monthlyPayment",
        "rate",
        "isInsuranceEnabled",
        "isSalaryClient",
    }

    for offer in offers:
        assert set(offer.keys()) == expected_fields


def test_loan_offers_have_valid_values(loan_request):

    response = client.post("/calculator/offers", json=loan_request)
    assert response.status_code == 200
    offers = response.json()

    for offer in offers:
        UUID(offer["statementId"])

        assert Decimal(str(offer["requestedAmount"])) > 0
        assert Decimal(str(offer["totalAmount"])) > 0
        assert Decimal(str(offer["monthlyPayment"])) > 0
        assert Decimal(str(offer["rate"])) > 0

        assert offer["term"] == loan_request["term"]

        assert Decimal(str(offer["requestedAmount"])) == Decimal(
            str(loan_request["amount"])
        )


def test_loan_offers_contain_all_insurance_combinations(loan_request):

    response = client.post("/calculator/offers", json=loan_request)
    assert response.status_code == 200
    offers = response.json()

    combinations = {
        (
            offer["isInsuranceEnabled"],
            offer["isSalaryClient"],
        )
        for offer in offers
    }

    expected_combinations = {
        (False, False),
        (False, True),
        (True, False),
        (True, True),
    }

    assert combinations == expected_combinations


def test_loan_offers_are_sorted_by_rate_descending(loan_request):

    response = client.post("/calculator/offers", json=loan_request)
    assert response.status_code == 200
    offers = response.json()

    rates = [
        Decimal(str(offer["rate"]))
        for offer in offers
    ]

    assert rates == sorted(rates, reverse=True)


def test_loan_offers_have_same_statement_id(loan_request):

    response = client.post("/calculator/offers", json=loan_request)
    assert response.status_code == 200
    offers = response.json()

    statement_ids = {
        offer["statementId"]
        for offer in offers
    }

    assert len(statement_ids) == 1