"""Main module."""

from fastapi import FastAPI

from src.api.routes.journeys import router as journeys_router

app = FastAPI()

app.include_router(journeys_router, prefix="/journeys")
