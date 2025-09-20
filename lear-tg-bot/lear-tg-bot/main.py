from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from handlers.add_command import add_en, add_ua
from handlers.echo_command import echo
from handlers.notify_task import notify_users_task
from handlers.start_command import start
from handlers.notify_command import add_notify
import asyncio

token="8312407763:AAERNh2KzR69c2SWrbUZ47JBJwBVnSuR4m8"

def main():
    app=Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_en", add_en))
    app.add_handler(CommandHandler("add_ua", add_ua))
    app.add_handler(CommandHandler("add_notify", add_notify))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    async def on_startup(application):
        asyncio.create_task(notify_users_task(application))

    app.post_init = on_startup
    app.run_polling()

if __name__=="__main__":
    main()
    
print("start")
input()
print("end")