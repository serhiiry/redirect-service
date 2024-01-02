from fastapi import FastAPI, Response
from .routers import health_check, redirect

app = FastAPI()

app.include_router(health_check.router)
app.include_router(redirect.router)
