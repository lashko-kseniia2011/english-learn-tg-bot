from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Word(BaseModel):
    english_word: str
    ukrainian_word: str
    user_id: int
    score: int = 0
    last_seen: Optional[datetime] = None
        
    