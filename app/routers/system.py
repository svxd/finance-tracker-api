from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def read_root():
    return {
        "message": "Finance Tracker API is running",
    }


@router.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@router.get("/version")
def version_check():
    return {
        "version": "0.1.0"
    }


@router.get("/about")
def about_info():
    return {
        "project": "Finance Tracker API",
        "purpose": "Backend sprint project for learning FastAPI"
    }
