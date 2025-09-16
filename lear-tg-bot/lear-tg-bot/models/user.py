from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    wait_word: Optional[str] = None