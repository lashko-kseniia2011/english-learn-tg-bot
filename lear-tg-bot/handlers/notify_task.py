import asyncio
from datetime import datetime
from telegram.ext import Application
from models.database import Database

from services.learning import start_learning_for_user


async def notify_users_task(application: Application):
    while True:
        database = Database.load()
        now = datetime.now()

        for user in database.users:
            if user.hp < 10:
                user.hp += 1
        database.save()

        for notify in database.notifies:
            if now.time().hour == notify.notify_time.hour and now.time().minute == notify.notify_time.minute:
                try:
                    await start_learning_for_user(notify.user_id, application)
                except Exception as e:
                    print(f"❌ Не вдалося надіслати повідомлення {notify.user_id}: {e}")
        await asyncio.sleep(60)