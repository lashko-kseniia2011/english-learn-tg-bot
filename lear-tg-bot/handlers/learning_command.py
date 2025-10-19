import random
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from models.database import Database
from services.learning import choose_word, get_words_for_today
from services.keyboards import main_menu_keyboard, learning_keyboard


async def learning_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, from_callback=False):
    database = Database.load()

    if from_callback:
        reply_target = update.callback_query.message
    else:
        reply_target = update.message

    user = next((u for u in database.users if u.id == update.effective_user.id), None)
    if not user or not user.wait_word:
        await reply_target.reply_text("Немає активного слова. Почніть навчання через головне меню.",
                                        reply_markup=main_menu_keyboard())
        return

    user_words = get_words_for_today(user.id, database.words)
    current_word = next((w for w in user_words if w.english_word == user.wait_word or w.ukrainian_word == user.wait_word), None)
    if not current_word:
        await reply_target.reply_text("Сталася помилка зі словом. Спробуйте почати заново.",
                                        reply_markup=main_menu_keyboard())
        user.wait_word = None
        database.save()
        return

    if from_callback:
        answer = context.user_data.get('last_answer', '').lower()
    else:
        answer = update.message.text.strip().lower()

    if user.direction == 'en_ua':
        correct = current_word.ukrainian_word.lower()
    else:
        correct = current_word.english_word.lower()

    if answer == correct:
        user.points+=10
        user.hp = min(user.hp+1, 10)
        current_word.score += 1
        current_word.last_seen = datetime.now()
        user_words.remove(current_word)
        await reply_target.reply_text(f"✅ Правильно! (Бал: {current_word.score})")
    else:
        user.hp = max(user.hp-1, 0)
        current_word.score = max(0, current_word.score - 1)
        await reply_target.reply_text(f"❌ Неправильно. Правильна відповідь: {correct} (Бал: {current_word.score})")

    current_word.last_seen = datetime.now()
    user.word_count -= 1

    if user.word_count > 0 and user.hp>0:
        next_word = choose_word(user_words)
        direction = random.choice(['en_ua', 'ua_en'])
        user.direction = direction
        if direction == 'en_ua':
            user.wait_word = next_word.ukrainian_word
            await reply_target.reply_text(f"Напиши переклад слова: {next_word.english_word}", reply_markup=learning_keyboard())
        else:
            user.wait_word = next_word.english_word
            await reply_target.reply_text(f"Напиши переклад слова: {next_word.ukrainian_word}", reply_markup=learning_keyboard())
    else:
        user.word_count = 0
        user.wait_word = None
        await reply_target.reply_text("🎉 Сеанс навчання завершено!", reply_markup=main_menu_keyboard())

    database.save()