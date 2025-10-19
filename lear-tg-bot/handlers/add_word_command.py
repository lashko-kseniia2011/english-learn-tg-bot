from telegram import Update
from telegram.ext import ContextTypes

from models.database import Database
from models.word import Word
from services.keyboards import add_word_keyboard
from services.translate import translate_word


async def add_word_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database.load()
    user_id = update.effective_user.id
    text = update.message.text.strip()

    user = next((u for u in database.users if u.id == user_id), None)
    if not user:
        await update.message.reply_text("Спочатку зареєструйтесь через /start")
        return

    if context.user_data['adding_word'] == 'en':
        new_word = Word(
            english_word=text,
            ukrainian_word=await translate_word(text),
            user_id=user_id,
            score=0,
            last_seen=None
        )
    else:
        new_word = Word(
            english_word=await translate_word(text, "uk", "en"),
            ukrainian_word=text,
            user_id=user_id,
            score=0,
            last_seen=None
        )

    database.words.append(new_word)
    database.save()

    await update.message.reply_text(f"Слово '{text}' додано! ✅", reply_markup=add_word_keyboard())
