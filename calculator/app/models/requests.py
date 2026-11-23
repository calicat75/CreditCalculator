from datetime import date
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

MIN_AMOUNT = Decimal("10000")
MAX_AMOUNT = Decimal("5000000")

MIN_TERM = 6
MAX_TERM = 60

MIN_AGE = 18
MAX_AGE = 65

NAME_PATTERN = r"^[A-Za-z]{2,30}$"
PASSPORT_SERIES_PATTERN = r"^\d{4}$"
PASSPORT_NUMBER_PATTERN = r"^\d{6}$"


class PersonalDataDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(
        alias="firstName",
        pattern=NAME_PATTERN,
    )
    last_name: str = Field(
        alias="lastName",
        pattern=NAME_PATTERN,
    )
    middle_name: str = Field(
        alias="middleName",
        pattern=NAME_PATTERN,
    )

    birthdate: date

    passport_series: str = Field(
        alias="passportSeries",
        pattern=PASSPORT_SERIES_PATTERN,
    )
    passport_number: str = Field(
        alias="passportNumber",
        pattern=PASSPORT_NUMBER_PATTERN,
    )

    @field_validator("birthdate")
    @classmethod
    def validate_birthdate(cls, value: date) -> date:
        today = date.today()

        age = (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )

        if not MIN_AGE <= age <= MAX_AGE:
            raise ValueError(
                f"Возраст заёмщика должен быть от {MIN_AGE} до {MAX_AGE} лет"
            )

        return value


class LoanStatementRequestDto(PersonalDataDto):
    amount: Decimal = Field(
        ge=MIN_AMOUNT,
        le=MAX_AMOUNT,
    )
    term: int = Field(
        ge=MIN_TERM,
        le=MAX_TERM,
    )

    email: EmailStr


class ScoringDataDto(PersonalDataDto):
    amount: Decimal = Field(
        ge=MIN_AMOUNT,
        le=MAX_AMOUNT,
    )
    term: int = Field(
        ge=MIN_TERM,
        le=MAX_TERM,
    )

    is_insurance_enabled: bool = Field(alias="isInsuranceEnabled")
    is_salary_client: bool = Field(alias="isSalaryClient")