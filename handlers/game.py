from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from services.gpt import get_openai_word
import random

router = Router()

word_list = [
    "время", "человек", "год", "день", "рука", "дело", "раз", "глаз", "жизнь", "голова",
    "друг", "дом", "слово", "место", "лицо", "сторона", "нога", "работа", "дверь", "конец",
    "город", "вопрос", "женщина", "земля", "машина", "ребёнок", "сила", "воздух", "мать", "отец",
    "вода", "стол", "ночь", "неделя", "путь", "свет", "комната", "язык", "минута", "право",
    "мир", "час", "тело", "утро", "стена", "любовь", "душа", "взгляд", "плечо", "папа",
    "мама", "школа", "ребята", "друг", "голос", "окно", "вечер", "письмо", "палец", "путь",
    "чувство", "мысль", "сердце", "рукав", "дерево", "река", "деньги", "сон", "половина", "небо",
    "сестра", "брат", "карман", "камень", "солнце", "снег", "нос", "зуб", "грудь", "волос",
    "пыль", "песок", "шаг", "след", "лист", "цветок", "трава", "огонь", "снег", "ветер",
    "пол", "кровать", "зеркало", "стул", "потолок", "полка", "ковёр", "шкаф", "книга", "тетрадь"
]

class GameStates(StatesGroup):
    mode = State()
    theme = State()
    difficulty = State()
    game = State()

game_data = {}

@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Выбери режим:\n1 — случайное слово\n2 — слово от ИИ (OpenAI)")
    await state.set_state(GameStates.mode)

@router.message(GameStates.mode)
async def select_mode(message: types.Message, state: FSMContext):
    mode = message.text.strip()
    if mode == "1":
        word = random.choice(word_list)
        await start_game(message, state, word)
    elif mode == "2":
        await message.answer("Введите тему:")
        await state.set_state(GameStates.theme)
    else:
        await message.answer("Введите 1 или 2.")

@router.message(GameStates.theme)
async def ask_difficulty(message: types.Message, state: FSMContext):
    await state.update_data(theme=message.text.strip())
    await message.answer("Введите уровень сложности (легкий, средний, сложный):")
    await state.set_state(GameStates.difficulty)

@router.message(GameStates.difficulty)
async def get_openai_word_and_start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    theme = data["theme"]
    difficulty = message.text.strip().lower()

    word = await get_openai_word(theme, difficulty)
    await start_game(message, state, word)

async def start_game(message: types.Message, state: FSMContext, word: str):
    word_completion = "_" * len(word)
    game_data[message.from_user.id] = {
        "word": word,
        "completion": word_completion,
        "guessed": [],
        "tries": 6
    }
    await state.set_state(GameStates.game)
    await message.answer(f"Игра началась!\nСлово: {word_completion}\nКоличество букв в слове: {len(word)}\nПопыток: 6\nВведите букву или слово:")

@router.message(GameStates.game)
async def process_guess(message: types.Message, state: FSMContext):
    guess = message.text.strip().lower()
    user_id = message.from_user.id

    if user_id not in game_data:
        await message.answer("Сначала начни игру: /start")
        return

    data = game_data[user_id]
    word = data["word"]
    completion = data["completion"]
    guessed = data["guessed"]
    tries = data["tries"]

    if guess in guessed:
        await message.answer("Вы уже вводили это.")
        return

    guessed.append(guess)

    if guess == word:
        await message.answer(f"Поздравляю, вы угадали слово: {word}")
        await state.clear()
        return

    if len(guess) == 1 and guess in word:
        new_completion = ''.join(
            guess if word[i] == guess else completion[i] for i in range(len(word))
        )
        data["completion"] = new_completion
        await message.answer(f"Буква угадана!\n{new_completion}")
    elif len(guess) == 1:
        data["tries"] -= 1
        await message.answer(f"Буквы нет. Осталось попыток: {data['tries']}")
    else:
        data["tries"] -= 1
        await message.answer(f"Слово не угадано. Осталось попыток: {data['tries']}")

    if data["completion"] == word:
        await message.answer(f"Вы победили! Слово: {word}")
        await state.clear()
    elif data["tries"] <= 0:
        await message.answer(f"Вы проиграли. Слово было: {word}")
        await state.clear()
