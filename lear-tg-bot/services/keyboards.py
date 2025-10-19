from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from models.word import Word


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Мої слова", callback_data="my_words")],
        [InlineKeyboardButton("▶️ Почати навчання", callback_data="start_learning")],
        [InlineKeyboardButton("⚙️ Налаштування", callback_data="settings")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("🏆 Лідерборд", callback_data="leaderboard")]
    ]
    return InlineKeyboardMarkup(keyboard)



def learning_keyboard():
    keyboard = [
        [InlineKeyboardButton("💡 Підказка", callback_data="show_hint")]
    ]
    return InlineKeyboardMarkup(keyboard)

def add_word_keyboard():
    keyboard = [
        [InlineKeyboardButton("➕ Додати слово українське слово", callback_data="add_ua")],
        [InlineKeyboardButton("➕ Додати слово англійське слово", callback_data="add_en")],
        [InlineKeyboardButton("➕ Додати 10 випадкових слів", callback_data="add_10_random")],
        [InlineKeyboardButton("➕ Додати 100 випадкових слів", callback_data="add_100_random")],
        [InlineKeyboardButton("⬅️ Головне меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def settings_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("➕ Додати час навчання", callback_data="add_notify_menu")],
        [InlineKeyboardButton("➖ Видалити час навчання", callback_data="remove_notify_menu")],
        [InlineKeyboardButton("📋 Показати всі сповіщення", callback_data="list_notifies")],
        [InlineKeyboardButton("⬅️ Головне меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


WORDS_PER_PAGE = 10

def get_words_keyboard(user_words: list[Word], page: int = 0) -> InlineKeyboardMarkup:
    start = page * WORDS_PER_PAGE
    end = start + WORDS_PER_PAGE
    page_words = user_words[start:end]

    keyboard = []

    for i, word in enumerate(page_words, start=start + 1):
        # Кнопки редагування та видалення
        keyboard.append([
            InlineKeyboardButton(f"✏️ {word.english_word}", callback_data=f"edit_word_{i-1}"),
            InlineKeyboardButton("🗑️", callback_data=f"delete_word_{i-1}")
        ])

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Попередня", callback_data=f"words_page_{page-1}"))
    if end < len(user_words):
        nav_buttons.append(InlineKeyboardButton("➡️ Наступна", callback_data=f"words_page_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append([InlineKeyboardButton("➕ Додати слово українське", callback_data="add_ua")])
    keyboard.append([InlineKeyboardButton("➕ Додати слово англійське", callback_data="add_en")])
    keyboard.append([InlineKeyboardButton("➕ Додати 10 випадкових слів", callback_data="add_10_random")])
    keyboard.append([InlineKeyboardButton("➕ Додати 100 випадкових слів", callback_data="add_100_random")])
    keyboard.append([InlineKeyboardButton("⬅️ Головне меню", callback_data="main_menu")])

    return InlineKeyboardMarkup(keyboard)