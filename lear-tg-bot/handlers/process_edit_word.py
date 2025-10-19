from telegram import Update
from telegram.ext import ContextTypes
from models.database import Database
from handlers.my_words_command import my_words

async def process_edit_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database.load()
    word_to_edit = context.user_data.get('editing_word')
    if not word_to_edit:
        await update.message.reply_text("Слово для редагування не знайдено.")
        return

    user_input = update.message.text.strip()

    if "-" not in user_input:
        await update.message.reply_text(
            "Неправильний формат. Введіть як: Англійське слово - Українське слово"
        )
        return

    english, ukrainian = map(str.strip, user_input.split("-", 1))
    word_to_edit.english_word = english
    word_to_edit.ukrainian_word = ukrainian
    database.words.append(word_to_edit)
    database.save()

    await update.message.reply_text(
        f"Слово успішно змінено: {english} — {ukrainian}"
    )

    await my_words(update, context)
