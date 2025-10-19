from telegram import Update
from telegram.ext import ContextTypes

from models.database import Database


async def edit_word_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    user_id = update.callback_query.from_user.id
    index = int(update.callback_query.data.split("_")[-1])

    database = Database.load()
    user_words = [w for w in database.words if w.user_id == user_id]

    if 0 <= index < len(user_words):
        context.user_data['editing_word'] = user_words[index]
        database.words.remove(user_words[index])
        database.save()
        await update.callback_query.message.reply_text(
            f"Введіть новий англійський і український переклад через дефіс (English - Ukrainian):"
        )
    else:
        await update.callback_query.message.reply_text("Неможливо редагувати слово. Некоректний індекс.")
