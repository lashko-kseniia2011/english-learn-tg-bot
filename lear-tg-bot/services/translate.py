from googletrans import Translator

translator = Translator()

async def translate_word(word: str, src: str = 'en', dest: str = 'uk'):
    try:
        result = await translator.translate(word, src=src, dest=dest)
        return result.text
    except Exception as e:
        print(f"Помилка при перекладі: {e}")
        return None

