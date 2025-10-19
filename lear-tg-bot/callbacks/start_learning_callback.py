from telegram import Update
from telegram.ext import ContextTypes
from services.learning import  start_learning_for_user


async def start_learning_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    user_id = update.callback_query.from_user.id

    try:
        await start_learning_for_user(user_id, context.application, reply_to=update.callback_query.message)
    except Exception as e:
        print(f"Помилка при старті навчання: {e}")

