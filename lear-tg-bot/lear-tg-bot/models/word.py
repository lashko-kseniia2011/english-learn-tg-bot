


class Word:
    english_word: str
    ukraine_word: str
    user_id: int
    
    def __init__(self, english_word: str, ukraine_word: str, user_id: int):
        self.english_word = english_word
        self.ukraine_word = ukraine_word
        self.user_id = user_id
        
    