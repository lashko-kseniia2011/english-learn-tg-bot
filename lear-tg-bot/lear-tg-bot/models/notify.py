from datetime import time
from pydantic import BaseModel

class Notify(BaseModel):
    notify_time: time
    user_id: int

    class Config:
        json_encoders = {
            time: lambda t: t.isoformat()
        }