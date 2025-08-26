from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

token=""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    await update.message.reply_text("Hy I am your bot")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    await update.message.reply_text(f"you write {update.message.text}")

def main():
    app=Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__=="__main__":
    main()
    
print("strat")
input()
print("end")