from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="API Authorization Research Lab",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "project": "API Authorization Research Lab",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
