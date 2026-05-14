from fastapi import FastAPI

from app.database import Base, engine
from app.routers import summary, system, transactions


app = FastAPI(
    title="Finance Tracker API",
    description="A small backend API for tracking personal finance transactions.",
    version="0.1.0",
)


Base.metadata.create_all(bind=engine)


app.include_router(system.router)
app.include_router(transactions.router)
app.include_router(summary.router)
