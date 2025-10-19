from telegram import Update
from telegram.ext import ContextTypes

async def add_word_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    language = update.callback_query.data.split("_")[1]
    context.user_data["adding_word"] = language

    text = "Введіть слово українською:" if language == "ua" else "Введіть слово англійською:"
    await update.callback_query.message.reply_text(text)

    return
