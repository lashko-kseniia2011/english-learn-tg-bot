from datetime import time

class Notify:
    notify: time
    user_id: int

    def __init__(self, notify: time, user_id: int):
        self.notify = notify
        self.user_id = user_id
