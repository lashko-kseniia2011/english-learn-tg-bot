from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from callbacks.add_notify_menu_callback import add_notify_menu_callback
from callbacks.add_random_callback import add_10_random_callback, add_100_random_callback
from callbacks.add_word_callback import add_word_callback
from callbacks.answer_callback import answer_callback
from callbacks.delete_word_callback import delete_word_callback
from callbacks.edit_word_callback import edit_word_callback
from callbacks.leaderboard_callback import leaderboard_callback
from callbacks.list_notifies_callback import list_notifies_callback
from callbacks.main_menu_callback import main_menu_callback
from callbacks.my_words_callback import my_words_callback
from callbacks.remove_notify_callback import remove_notify_callback
from callbacks.remove_notify_menu_callback import remove_notify_menu_callback
from callbacks.settings_callback import settings_callback
from callbacks.show_hint_callback import show_hint_callback
from callbacks.start_learning_callback import start_learning_callback
from callbacks.stats_callback import stats_callback
from handlers.my_words_command import my_words
from handlers.notify_task import notify_users_task
from handlers.start_command import start
from handlers.notify_command import add_notify
import asyncio

from handlers.text_handler import text_handler

token="8312407763:AAERNh2KzR69c2SWrbUZ47JBJwBVnSuR4m8"

def main():
    app=Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("my_words", my_words))
    app.add_handler(CommandHandler("add_notify", add_notify))
    app.add_handler(CallbackQueryHandler(my_words_callback, pattern="^(my_words|words_page_\\d+)$"))
    app.add_handler(CallbackQueryHandler(add_word_callback, pattern="^add_(ua|en)$"))
    app.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(show_hint_callback, pattern="^show_hint$"))
    app.add_handler(CallbackQueryHandler(start_learning_callback, pattern="^start_learning$"))
    app.add_handler(CallbackQueryHandler(answer_callback, pattern="^answer_"))
    app.add_handler(CallbackQueryHandler(settings_callback, pattern="^settings$"))
    app.add_handler(CallbackQueryHandler(add_notify_menu_callback, pattern="^add_notify_menu$"))
    app.add_handler(CallbackQueryHandler(remove_notify_menu_callback, pattern="^remove_notify_menu$"))
    app.add_handler(CallbackQueryHandler(list_notifies_callback, pattern="^list_notifies$"))
    app.add_handler(CallbackQueryHandler(remove_notify_callback, pattern="^remove_notify_"))
    app.add_handler(CallbackQueryHandler(leaderboard_callback, pattern="^leaderboard$"))
    app.add_handler(CallbackQueryHandler(stats_callback, pattern="^stats$"))
    app.add_handler(CallbackQueryHandler(add_10_random_callback, pattern="^add_10_random$"))
    app.add_handler(CallbackQueryHandler(add_100_random_callback, pattern="^add_100_random$"))
    app.add_handler(CallbackQueryHandler(delete_word_callback, pattern=r"^delete_word_\d+$"))
    app.add_handler(CallbackQueryHandler(edit_word_callback, pattern=r"^edit_word_\d+$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    async def on_startup(application):
        asyncio.create_task(notify_users_task(application))

    app.post_init = on_startup
    app.run_polling()

if __name__=="__main__":
    main()