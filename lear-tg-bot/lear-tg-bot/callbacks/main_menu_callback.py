from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from services.keyboards import main_menu_keyboard


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Головне меню:",
        reply_markup=main_menu_keyboard()
    )

