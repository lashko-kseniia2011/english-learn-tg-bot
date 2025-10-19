from telegram import Update
from telegram.ext import ContextTypes


async def add_notify_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Введіть час у форматі HH:MM:SS для додавання сповіщення."
    )
    context.user_data['adding_notify'] = True