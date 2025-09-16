from pydantic import BaseModel


class Word(BaseModel):
    english_word: str
    ukraine_word: str
    user_id: int
        
    