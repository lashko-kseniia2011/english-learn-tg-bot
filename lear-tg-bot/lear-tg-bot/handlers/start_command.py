from telegram import Update
from telegram.ext import ContextTypes
from models.user import User

from models.database import Database

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database()
    user = update.effective_user
    new_user = User(user.id, user.first_name, user.last_name, user.username)
    database.users.append(new_user)
    print(f"Id - {new_user.id}, First Name - {new_user.first_name}, last name - {new_user.last_name}, username - {new_user.username}")
    await update.message.reply_text(f"Hello {new_user.first_name}")