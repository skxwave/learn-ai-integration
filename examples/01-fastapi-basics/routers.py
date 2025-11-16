from fastapi.routing import APIRouter

from .models import User

router = APIRouter()


@router.get("/hello")
async def hello_world():
    return {"message": "Hello world! Remembering fastapi again"}


@router.get("/hello/{name}")
async def hello_name(name: str):
    return {"message": f"Hello {name}"}


@router.post("/create_user")
async def create_user(user: User):
    return {
        "message": f"User '{user.username}' created!",
        "result": user,
    }
