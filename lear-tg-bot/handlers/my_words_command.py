from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from models.database import Database
from services.keyboards import add_word_keyboard, get_words_keyboard


async def my_words(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0):
    if update.callback_query:
        user_id = update.callback_query.from_user.id
        message = update.callback_query.message
        await update.callback_query.answer()
    else:
        user_id = update.effective_user.id
        message = update.message

    database = Database.load()
    user = next((u for u in database.users if u.id == user_id), None)

    if not user:
        text = "Спочатку потрібно зареєструватися, щоб почати додавати слова."
        keyboard = [[InlineKeyboardButton("🚀 Реєстрація", callback_data="start")]]
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    user_words = [w for w in database.words if w.user_id == user_id]
    if not user_words:
        text = "У вас ще немає слів для вивчення. Додайте нові слова, щоб почати навчання:"
        await message.reply_text(text, reply_markup=get_words_keyboard(user_words))
        return

    start = page * 10
    end = start + 10
    page_words = user_words[start:end]

    text = "Ваші слова для вивчення:\n\n"
    for i, word in enumerate(page_words, start=start + 1):
        rank = "🟩" if word.score >= 6 else "🟨" if word.score >= 3 else "🟥"
        last_seen_str = word.last_seen.strftime("%d.%m.%Y") if word.last_seen else "ще не вчили"
        text += f"{i}. {word.english_word} — {word.ukrainian_word} {rank} (Бал: {word.score}, Останній раз: {last_seen_str})\n"

    # Відправляємо повідомлення з клавіатурою
    await message.reply_text(text, reply_markup=get_words_keyboard(user_words, page))

    