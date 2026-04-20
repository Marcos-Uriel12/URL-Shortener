from fastapi import FastAPI
from app.routers import urls
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(urls.router)