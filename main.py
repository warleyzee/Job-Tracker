# app/main.py
from fastapi import FastAPI
from routes.route_application import router as application_router

app = FastAPI(title="Job Tracker")

app.include_router(application_router)


@app.get("/health")
def health():
    return {"status": "ok"}
