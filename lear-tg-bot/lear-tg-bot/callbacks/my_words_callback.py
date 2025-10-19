from telegram import Update
from telegram.ext import ContextTypes

from handlers.my_words_command import my_words
import re

async def my_words_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback_data = update.callback_query.data
    match = re.match(r"words_page_(\d+)", callback_data)
    page = int(match.group(1)) if match else 0

    await my_words(update, context, page=page)
