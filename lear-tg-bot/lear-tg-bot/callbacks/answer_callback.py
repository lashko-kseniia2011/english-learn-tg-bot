from telegram import Update
from telegram.ext import ContextTypes

from handlers.learning_command import learning_handler


async def answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_answer = query.data.replace("answer_", "")
    context.user_data['last_answer'] = user_answer
    await learning_handler(update, context, from_callback=True)
