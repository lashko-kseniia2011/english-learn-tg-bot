import json
import os

from pydantic import BaseModel, Field

from models.user import User
from models.word import Word
from models.notify import Notify

class Database(BaseModel):
    users: list[User] = Field(default_factory=list)
    words: list[Word] = Field(default_factory=list)
    notifies: list[Notify] = Field(default_factory=list)

    @classmethod
    def load(cls, filename: str = "db.json") -> "Database":
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(**data)
        else:
            return cls()

    def save(self, filename: str = "db.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(), f, ensure_ascii=False, indent=4, default=str)
