from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from models.database import Database
from models.notify import Notify

async def add_notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database.load()
    if len(context.args) == 1:
        time_str = context.args[0]
    else:
        await update.message.reply_text(f"Не правильний формат")
        return

    time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
    new_notify = Notify(notify_time=time_obj, user_id=update.effective_user.id)
    print(f"додали новий нагадувальник на {time_str}")
    database.notifies.append(new_notify)
    database.save()
    await update.message.reply_text(f"Нагадування {time_str} успішно додано")
