from fastapi import FastAPI
from app.routes.crypto import router as crypto_router

app = FastAPI()

app.include_router(crypto_router)