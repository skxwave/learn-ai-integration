from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """
    User Schema
    """
    model_config = {
        "extra": "forbid",
        "str_max_length": 256,
        "str_min_length": 3,
        "str_strip_whitespace": True,
        "str_to_lower": True,
    }

    username: str = Field(min_length=5, default="your_username")
    email: EmailStr = Field(default=None)
    first_name: str | None
    last_name: str | None
