import asyncio
from datetime import datetime, timedelta
from telegram.ext import Application
from models.database import Database
from models.word import Word
import random


async def notify_users_task(application: Application):
    while True:
        database = Database.load()
        now = datetime.now()
        for notify in database.notifies:
            if (now.time().hour == notify.notify_time.hour
                    and now.time().minute == notify.notify_time.minute) :
                try:
                    print(database.words)
                    print(database.notifies)
                    words = list(filter(lambda word: word.user_id == notify.user_id,database.words))
                    random_word: Word = random.choice(words)
                    await application.bot.send_message(
                        chat_id=notify.user_id,
                        text=f"Напиши переклад слова {random_word.ukraine_word}"
                    )
                    user = list(filter(lambda user: user.id == notify.user_id, database.users))[0]
                    user.wait_word = random_word.english_word
                    user.word_count = 10
                    database.save()
                except Exception as e:
                    print(f"❌ Не вдалося надіслати повідомлення {notify.user_id}: {e}")
        await asyncio.sleep(60)