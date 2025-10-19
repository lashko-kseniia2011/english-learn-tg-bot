from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    direction: Optional[str] = None
    wait_word: Optional[str] = None
    word_count: int = 0
    hp: int = 10
    points: int = 0