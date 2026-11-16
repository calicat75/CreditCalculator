from datetime import date
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

class LoanStatementRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    amount: Decimal = Field(gt=0)
    term: int = Field(gt=0)

    first_name: str = Field(alias="firstName", min_length=1)
    last_name: str = Field(alias="lastName", min_length=1)
    middle_name: str = Field(alias="middleName", min_length=1)

    email: EmailStr
    birthdate: date

    passport_series: str = Field(
        alias="passportSeries",
        pattern=r"^\d{4}$",
    )
    passport_number: str = Field(
        alias="passportNumber",
        pattern=r"^\d{6}$",
    )

    @field_validator("birthdate")
    @classmethod
    def validate_birthdate(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("Birthdate must be in the past")
        return value

class ScoringDataDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    amount: Decimal = Field(gt=0)
    term: int = Field(gt=0)

    first_name: str = Field(alias="firstName", min_length=1)
    last_name: str = Field(alias="lastName", min_length=1)
    middle_name: str = Field(alias="middleName", min_length=1)

    birthdate: date

    passport_series: str = Field(
        alias="passportSeries",
        pattern=r"^\d{4}$",
    )
    passport_number: str = Field(
        alias="passportNumber",
        pattern=r"^\d{6}$",
    )

    is_insurance_enabled: bool = Field(alias="isInsuranceEnabled")
    is_salary_client: bool = Field(alias="isSalaryClient")

    @field_validator("birthdate")
    @classmethod
    def validate_birthdate(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("Birthdate must be in the past")
        return value