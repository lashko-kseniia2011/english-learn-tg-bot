from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime
from models.database import Database
from services.keyboards import main_menu_keyboard


async def stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    database = Database.load()
    user_id = update.callback_query.from_user.id
    user = next((u for u in database.users if u.id == user_id), None)

    if not user:
        await update.callback_query.message.reply_text(
            "Спочатку зареєструйтесь через /start",
            reply_markup=main_menu_keyboard()
        )
        return

    user_words = [w for w in database.words if w.user_id == user_id]

    today = datetime.now().date()
    learned_today = [w for w in user_words if w.last_seen and w.last_seen.date() == today]

    stats_text = (
        "📊 <b>Ваша статистика</b>\n\n"
        f"💰 <b>Бали:</b> {user.points}\n"
        f"❤️ <b>Життя (HP):</b> {user.hp}/10\n"
        f"📚 <b>Всього слів:</b> {len(user_words)}\n"
        f"⏳ <b>Вивчено сьогодні:</b> {len(learned_today)}\n"
        f"📝 <b>Можна ще сьогодні вивчити:</b> {max(0, len(user_words) - len(learned_today))}\n"
    )

    await update.callback_query.message.reply_text(
        stats_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Головне меню", callback_data="main_menu")]
        ])
    )
