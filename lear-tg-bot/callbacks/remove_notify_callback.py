from telegram import Update
from telegram.ext import ContextTypes

from models.database import Database
from services.keyboards import settings_keyboard


async def remove_notify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    data = update.callback_query.data
    try:
        index = int(data.split("_")[-1])
    except ValueError:
        await update.callback_query.message.reply_text("Помилка при видаленні нагадування.", reply_markup=settings_keyboard())
        return

    database = Database.load()
    if 0 <= index < len(database.notifies):
        removed = database.notifies.pop(index)
        database.save()
        await update.callback_query.message.reply_text(
            f"Нагадування на {removed.notify_time.strftime('%H:%M:%S')} видалено ✅", reply_markup=settings_keyboard()
        )
    else:
        await update.callback_query.message.reply_text("Невірний індекс нагадування.", reply_markup=settings_keyboard())