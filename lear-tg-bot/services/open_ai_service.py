import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

async def hint(word: str) -> str:
    messages: list[ChatCompletionUserMessageParam] = [
        ChatCompletionUserMessageParam(
            content=f"Напиши речення в якому буде слово {word} англійською. Щоб я міг здогадатись переклад на українську. Але не пиши сам переклад",
            role="user")
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50,
            temperature=0.7
        )
        sentence = response.choices[0].message.content
        return sentence
    except Exception as e:
        print(f"Помилка генерації підказки: {e}")
        return f"Example sentence with the word '{word}'"

async def generate_new_words(existing_words: list[str], count: int = 10) -> list[str]:
    prompt = (
        f"Give me {count} simple English words suitable for a beginner. "
        f"Do not include these words: {', '.join(existing_words)}. "
        f"Return only the words separated by commas. No digits, only words."
    )

    messages: list[ChatCompletionUserMessageParam] = [
        ChatCompletionUserMessageParam(
            content=prompt,
            role="user"
        )
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        text = response.choices[0].message.content
        new_words = [w.strip() for w in text.split(",") if w.strip()]
        return new_words
    except Exception as e:
        print(f"Помилка генерації нових слів: {e}")
        return []
