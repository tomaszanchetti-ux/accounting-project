from fastapi import FastAPI

app = FastAPI(
    title="Accounting Reconciliation MVP API",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "service": "accounting-mvp-api",
        "status": "ok",
    }

