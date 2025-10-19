import random
from datetime import datetime

from telegram import Message

from models.database import Database
from models.word import Word
from services.keyboards import learning_keyboard, main_menu_keyboard

def get_words_for_today(user_id: int, words: list[Word]):
    today = datetime.today().date()
    available_words = [
        w for w in words
        if w.user_id == user_id and (not w.last_seen or w.last_seen.date() < today)
    ]
    return available_words

async def start_learning_for_user(user_id: int, application, reply_to: Message = None):
    database = Database.load()
    user = next((u for u in database.users if u.id == user_id), None)
    if not user:
        if reply_to:
            await reply_to.reply_text("Спочатку зареєструйтесь через /start")
        return

    if user.hp <= 0:
        message = "❌ У вас закінчилися життя! Зачекайте, поки вони відновляться, або спробуйте пізніше."
        if reply_to:
            await reply_to.reply_text(message)
        return

    user_words = get_words_for_today(user_id, database.words)
    if not user_words:
        if reply_to:
            await reply_to.reply_text(
                "У вас ще немає слів для навчання. Додайте слова через меню.",
                reply_markup=main_menu_keyboard()
            )
        return

    user.word_count = min(5, len(user_words))
    direction = random.choice(['en_ua', 'ua_en'])
    chosen_word = choose_word(user_words)
    user.direction = direction

    if direction == 'en_ua':
        user.wait_word = chosen_word.ukrainian_word
        text = f"Починаємо навчання! Напиши переклад слова: {chosen_word.english_word}"
    else:
        user.wait_word = chosen_word.english_word
        text = f"Починаємо навчання! Напиши переклад слова: {chosen_word.ukrainian_word}"

    database.save()

    if reply_to:
        await reply_to.reply_text(text, reply_markup=learning_keyboard())
    else:
        await application.bot.send_message(chat_id=user_id, text=text, reply_markup=learning_keyboard())

def choose_word(user_words):
    weights = []
    now = datetime.now()
    for w in user_words:
        days_since_last = (now - w.last_seen).days if w.last_seen else 30
        weight = max(1, 10 - w.score) * (1 + days_since_last / 7)
        weights.append(weight)
    return random.choices(user_words, weights=weights, k=1)[0]