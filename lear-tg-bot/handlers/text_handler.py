from telegram import Update
from telegram.ext import ContextTypes

from handlers.add_word_command import add_word_text
from handlers.learning_command import learning_handler
from handlers.notify_command import add_notify
from handlers.process_edit_word import process_edit_word


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'adding_word' in context.user_data:
        await add_word_text(update, context)
        context.user_data.pop('adding_word')
    elif 'adding_notify' in context.user_data:
        await add_notify(update, context)
        context.user_data.pop('adding_notify')
    elif 'editing_word' in context.user_data:
        await process_edit_word(update, context)
        context.user_data.pop('editing_word')
    else:
        await learning_handler(update, context)