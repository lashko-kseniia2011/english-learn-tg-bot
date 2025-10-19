import random
from telegram import Update
from telegram.ext import ContextTypes

from models.database import Database
from models.word import Word
from services.keyboards import main_menu_keyboard
from services.open_ai_service import generate_new_words
from services.translate import translate_word

async def add_random_words(update: Update, context: ContextTypes.DEFAULT_TYPE, count: int):
    database = Database.load()
    user_id = update.callback_query.from_user.id

    user = next((u for u in database.users if u.id == user_id), None)
    if not user:
        await update.callback_query.message.reply_text("Спочатку зареєструйтесь через /start")
        return

    random_words = await generate_new_words([w.english_word for w in database.words if w.user_id == user_id], count)

    added_words = []
    for _ in range(count):
        word_text = random.choice(random_words)
        if any(w.english_word == word_text for w in database.words if w.user_id == user_id):
            continue

        new_word = Word(
            english_word=word_text,
            ukrainian_word=await translate_word(word_text),
            user_id=user_id,
            score=0
        )
        database.words.append(new_word)
        added_words.append(word_text)

    database.save()

    if added_words:
        await update.callback_query.message.reply_text(
            f"Додано слова: {', '.join(added_words)} ✅",
            reply_markup=main_menu_keyboard()
        )
    else:
        await update.callback_query.message.reply_text(
            "Всі обрані слова вже є у вашому словнику.",
            reply_markup=main_menu_keyboard()
        )

async def add_10_random_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await add_random_words(update, context, count=10)

async def add_100_random_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await add_random_words(update, context, count=100)
