from fastapi import FastAPI

from configs.settings import settings
from routes import api_router

app = FastAPI(title=settings.title)
app.include_router(api_router)
