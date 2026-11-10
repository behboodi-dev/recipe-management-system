
from fastapi import FastAPI


app = FastAPI(
    title="Recipe Management System API",
    description="API for managing recipes, users, and favorites.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Recipe Management System API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
