from models.user import User
from models.word import Word
from models.notify import Notify

class Database():
    _instance = None
    users: list[User]
    words: list[Word]
    notifies: list[Notify]
    
    def __init__(self):
        self.users=[]
        self.words=[]
        self.notifies=[]
        
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
