from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from handlers.add_command import add_en, add_ua
from handlers.start_command import start
from handlers.notify_command import add_notify


token="8312407763:AAERNh2KzR69c2SWrbUZ47JBJwBVnSuR4m8"
 
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    await update.message.reply_text(f"you write {update.message.text}")

def main():
    app=Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_en", add_en))
    app.add_handler(CommandHandler("add_ua", add_ua))
    app.add_handler(CommandHandler("add_notify", add_notify))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__=="__main__":
    main()
    
print("start")
input()
print("end")