from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from models.database import Database


async def remove_notify_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    database = Database.load()
    user_id = update.callback_query.from_user.id
    user_notifies = [n for n in database.notifies if n.user_id == user_id]

    if not user_notifies:
        await update.callback_query.message.reply_text("У вас немає сповіщень для видалення.")
        return

    keyboard = [
        [InlineKeyboardButton(n.notify_time.strftime("%H:%M:%S"), callback_data=f"remove_notify_{i}")]
        for i, n in enumerate(user_notifies)
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="settings")])
    await update.callback_query.message.reply_text(
        "Оберіть сповіщення для видалення:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )