from fastapi import FastAPI

app = FastAPI(
    title="Finance Tracker API",
    description="A small backend API for tracking personal finance transactions.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Finance Tracker API is running",
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

@app.get("/version")
def version_check():
    return {
        "version": "0.1.0"
    }

@app.get("/about")
def about_info():
    return {
        "project": "Finance Tracker API",
        "purpose": "Backend sprint project for learning FastAPI"
    }
