from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from models.database import Database
from models.notify import Notify
from services.keyboards import settings_keyboard


async def add_notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database.load()
    time_str = update.message.text.strip()  # беремо текст повідомлення

    try:
        time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
    except ValueError:
        await update.message.reply_text("❌ Неправильний формат. Використовуйте HH:MM:SS")
        return

    new_notify = Notify(notify_time=time_obj, user_id=update.effective_user.id)
    database.notifies.append(new_notify)
    database.save()

    await update.message.reply_text(f"✅ Нагадування на {time_str} успішно додано", reply_markup=settings_keyboard())
