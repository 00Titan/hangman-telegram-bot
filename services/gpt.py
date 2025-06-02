import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_openai_word(theme: str, difficulty: str) -> str:
    prompt = f"Сгенерируй одно русское существительное по теме «{theme}» и уровню сложности «{difficulty}». Без объяснений, только слово."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.8
        )
        word = response.choices[0].message['content'].strip().lower()
        if word.isalpha():
            return word
        return "время"
    except Exception as e:
        print(f"Ошибка OpenAI: {e}")
        return "время"
