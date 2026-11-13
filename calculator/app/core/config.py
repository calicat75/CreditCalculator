from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_rate: float = 20.0

    insurance_discount: float = 3.0
    salary_discount: float = 1.0

    insurance_cost: float = 100000.0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()