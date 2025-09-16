from datetime import time

class Notify:
    notify_time: time
    user_id: int

    def __init__(self, notify: time, user_id: int):
        self.notify_time = notify
        self.user_id = user_id


    def __repr__(self):
        return f"notify_time - {self.notify_time}, user_id - {self.user_id}"
