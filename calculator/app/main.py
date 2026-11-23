from fastapi import FastAPI

from app.api.endpoints.calculator import router as calculator_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Credit Calculator",
    description="Микросервис расчета кредитных предложений и параметров кредита",
    version="1.0.0",
)
app.include_router(calculator_router)