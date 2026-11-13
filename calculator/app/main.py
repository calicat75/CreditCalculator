from fastapi import FastAPI

app = FastAPI(
    title="Credit Calculator",
    description="Микросервис расчёта кредитных предложений",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}