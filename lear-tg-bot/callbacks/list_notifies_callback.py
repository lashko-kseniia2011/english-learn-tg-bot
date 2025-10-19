from telegram import Update
from telegram.ext import ContextTypes

from models.database import Database


async def list_notifies_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    database = Database.load()
    user_id = update.callback_query.from_user.id
    user_notifies = [n for n in database.notifies if n.user_id == user_id]

    if not user_notifies:
        await update.callback_query.message.reply_text("У вас немає сповіщень.")
        return

    text = "Ваші сповіщення:\n" + "\n".join(n.notify_time.strftime("%H:%M:%S") for n in user_notifies)
    await update.callback_query.message.reply_text(text)