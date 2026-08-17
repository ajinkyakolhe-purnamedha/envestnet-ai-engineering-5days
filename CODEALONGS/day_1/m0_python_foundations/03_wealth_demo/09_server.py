from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    """Confirm that the application is running."""
    return {"status": "ok"}
