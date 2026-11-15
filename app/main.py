"""
Main entry point for the Recipe Management System API.

Initializes the FastAPI application, includes route modules, and defines
basic health check endpoints.
"""

from fastapi import FastAPI

from app.api.routes.recipes import router as recipes_router


app = FastAPI(
    title="Recipe Management System API",
    description="API for managing recipes, users, and favorites.",
    version="1.0.0",
)


app.include_router(recipes_router)


@app.get("/")
def root():
    """
    Root endpoint.

    Returns a welcome message to confirm the API is running.
    """
    return {
        "message": "Welcome to Recipe Management System API"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.

    Used to verify that the API server is up and responding.
    """
    return {
        "status": "ok"
    }