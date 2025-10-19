from telegram import Update
from telegram.ext import ContextTypes
from services.keyboards import settings_keyboard


async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    await update.callback_query.message.reply_text(
        "Налаштування сповіщень:",
        reply_markup=settings_keyboard()
    )