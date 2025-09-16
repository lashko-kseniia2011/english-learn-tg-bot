
from telegram import Update
from telegram.ext import ContextTypes

from models.database import Database
from models.word import Word


async def add_en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database.load()
    if len(context.args)==1:
        new_en_word = context.args[0]
    else:
        await update.message.reply_text(f"Можна додати тільки одне слово")
        return 
    #todo get ukraine word from google translate
    new_word = Word(english_word=new_en_word, ukraine_word="", user_id=update.effective_user.id)
    print(f"engilsh - {new_word.english_word}, ukraine - {new_word.ukraine_word}, user_id - {new_word.user_id}")
    database.words.append(new_word)
    database.save()
    await update.message.reply_text(f"Slovo {new_word.english_word} uspishno dodano")
    

async def add_ua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database.load()
    if len(context.args)==1:
        new_ua_word = context.args[0]
    else:
        await update.message.reply_text(f"Можна додати тільки одне слово")
        return 
    #todo get ukraine word from google translate
    new_word = Word(english_word="", ukraine_word=new_ua_word, user_id=update.effective_user.id)
    print(f"engilsh - {new_word.english_word}, ukraine - {new_word.ukraine_word}, user_id - {new_word.user_id}")
    database.words.append(new_word)
    database.save()
    await update.message.reply_text(f"Slovo {new_word.ukraine_word} Успішно додано")

    