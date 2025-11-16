from fastapi import FastAPI
from .routers import router

app = FastAPI(
    title="AI Integration Examples",
    description="Collection of AI integration examples using LangChain, LangGraph, and FastAPI",
    version="1.0.0"
)

app.include_router(
    router=router,
    prefix="/fastapi-basics",
    tags=["FastAPI Basics"]
)