from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models.user import User

from models.database import Database
from services.keyboards import main_menu_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database.load()
    user = update.effective_user


    existing_user = next((u for u in database.users if u.id == user.id), None)
    if existing_user is None:
        new_user = User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username
        )
        database.users.append(new_user)
        database.save()
        name = new_user.first_name
        print(f"New user added: Id - {new_user.id}, Name - {new_user.first_name} {new_user.last_name}, username - {new_user.username}")
    else:
        name = existing_user.first_name
        print(f"Existing user: Id - {existing_user.id}, Name - {existing_user.first_name} {existing_user.last_name}")


    await update.message.reply_text(
        f"Привіт, {name}! 👋\nВибери опцію нижче, щоб почати:", reply_markup=main_menu_keyboard())