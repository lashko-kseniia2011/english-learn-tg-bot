from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from models.database import Database
from services.keyboards import main_menu_keyboard


async def leaderboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    database = Database.load()
    users = sorted(database.users, key=lambda u: getattr(u, "points", 0), reverse=True)

    if not users:
        await update.callback_query.message.reply_text(
            "😔 Поки що немає користувачів у таблиці лідерів.",
            reply_markup=main_menu_keyboard()
        )
        return

    top_10 = users[:10]

    leaderboard_text = "🏆 <b>Таблиця лідерів</b>\n\n"
    for i, user in enumerate(top_10, start=1):
        name = user.first_name or user.username or f"Користувач {user.id}"
        leaderboard_text += f"{i}. {name} — {user.points} балів\n"

    await update.callback_query.message.reply_text(
        leaderboard_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Головне меню", callback_data="main_menu")]
        ])
    )
