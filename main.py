from fastapi import FastAPI

from day_1.day_one import router

app = FastAPI()
app.include_router(
    router=router,
    prefix="/day_one",
)
