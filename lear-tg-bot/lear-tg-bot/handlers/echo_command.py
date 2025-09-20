from telegram import Update
from telegram.ext import ContextTypes
import random
from models.database import Database
from models.word import Word

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    database = Database.load()
    user = list(filter(lambda x : x.id == update.effective_user.id, database.users))[0]
    if user.wait_word == update.message.text:
        await update.message.reply_text(f"Правильно")
        if user.word_count>0:
            words = list(filter(lambda word: word.user_id == user.id, database.words))
            random_word: Word = random.choice(words)
            await update.message.reply_text(f"Напиши переклад слова {random_word.ukraine_word}")
            user.wait_word = random_word.english_word
            user.word_count-=1
            database.save()
        else:
            await update.message.reply_text(f"Успішно повчився сьогодні")
    else:
        await update.message.reply_text(f"Неправильно, спробуй ще раз")

