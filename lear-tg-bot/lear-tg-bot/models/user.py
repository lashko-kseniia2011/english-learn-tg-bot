class User:
    id: int
    first_name: str
    last_name: str
    username: str
    wait_word: str = None
    
    def __init__ (self,  id: int, first_name: str, last_name: str, username: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username