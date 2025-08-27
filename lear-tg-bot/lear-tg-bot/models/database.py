from models.user import User
from models.word import Word

class Database():
    _instance = None
    users: list[User]
    words: list[Word]
    
    def __init__(self):
        self.users=[]
        self.words=[]
        
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
