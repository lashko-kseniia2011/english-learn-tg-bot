from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random
from models.database import Database
from services.learning import get_words_for_today
from services.open_ai_service import hint
from services.keyboards import main_menu_keyboard


async def show_hint_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    user_id = update.callback_query.from_user.id
    database = Database.load()

    user = next((u for u in database.users if u.id == user_id), None)
    if not user or not user.wait_word:
        await update.callback_query.message.reply_text(
            "Немає активного слова для підказки.",
            reply_markup=main_menu_keyboard()
        )
        return

    if user.points < 20:
        await update.callback_query.message.reply_text(
            f"❌ У вас недостатньо балів для підказки. "
            f"Потрібно 20, а у вас лише {user.points}."
        )
        return

    user.points -= 20
    database.save()

    user_words = get_words_for_today(user.id, database.words)
    current_word = next((w for w in user_words if w.english_word == user.wait_word or w.ukrainian_word == user.wait_word), None)
    if not current_word:
        await update.callback_query.message.reply_text(
            "Не вдалося знайти слово. Спробуйте почати заново.",
            reply_markup=main_menu_keyboard()
        )
        user.wait_word = None
        database.save()
        return

    if user.direction == "en_ua":
        text_example = await hint(user.wait_word)
        await update.callback_query.message.reply_text(f"💡 Підказка:\n{text_example}")
    else:
        all_english_words = [w.english_word for w in database.words if w.user_id == user.id and w != current_word]
        options = random.sample(all_english_words, k=min(3, len(all_english_words)))
        options.append(current_word.english_word)
        random.shuffle(options)

        keyboard = [[InlineKeyboardButton(opt, callback_data=f"answer_{opt}")] for opt in options]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(
            "💡 Підказка: оберіть правильний варіант:",
            reply_markup=reply_markup
        )
