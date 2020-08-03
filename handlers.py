from load_all import dp
from async_database import db
from states import AddWord, Testing
import keyboards as kb

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from emoji import demojize


@dp.message_handler(commands=['start', 'help'])
@dp.message_handler(lambda msg: msg.text.lower()[1:-1] == 'помощь')
async def subscribe(message: types.Message):
    if await db.async_get_user(user_id=message.from_user.id) is None:
        await db.async_add_user_to_database(user_id=message.from_user.id)

    words_count = await db.async_get_words_count()

    await message.answer(f'Приветствую, <b><i>{message.from_user.username}</i></b>!\n\nДанный бот предназначен для '
                         f'того, чтобы '
                         f'закрепить твой словарный запас. Добавляй слова с переводом и проходи тесты, на основе этих '
                         f'слов.\n\n<code>Тестирование</code> - пройти тестирование по словам из базы данных по '
                         f'различным категориям.\n\nВсего слов '
                         f'добавлено: <b>{words_count}</b>\n\n'
                         f'<code>Добавить слово</code> - добавить слово в существующую базу данных.',
                         reply_markup=kb.kbStart, parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: True, text='back', state='*')
async def back_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Возвращаюсь в главное меню...', reply_markup=kb.kbStart)
    await state.finish()


@dp.message_handler(lambda msg: msg.text.lower() == 'вернуться в главное меню', state='*')
async def go_to_main_menu(message: types.Message, state: FSMContext):
    await message.answer("Возвращаюсь в главное меню...", reply_markup=kb.kbStart)
    await state.finish()


@dp.message_handler(commands=['add_word'], state="*")
@dp.message_handler(lambda msg: msg.text.lower()[:-2] == 'добавить слово', state="*")
async def add_word_step1(message: types.Message):
    await message.answer("Вы перешли в меню добавления слова.", reply_markup=ReplyKeyboardRemove())
    await message.answer("Пожалуйста, выберите категорию, в которую вы хотите добавить слово.",
                         reply_markup=kb.categories)
    await AddWord.waiting_for_category.set()


@dp.callback_query_handler(state=AddWord.waiting_for_category)
async def add_word_step2(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=call.data)
    await call.message.answer("Пожалуйста, введите одно или несколько слов, в формате \"Слово - "
                              "перевод\". Каждое слово с "
                              "перводом нужно писать с новой строки.")
    await AddWord.write_to_database.set()


@dp.message_handler(state=AddWord.write_to_database)
async def add_word_step3(message: types.Message, state: FSMContext):
    added_words = ''
    if not ' - ' in message.text:
        await message.answer("Вы ввели слова в неправильном формате. Пожалуйста, напишите их, как\n\n<code>Слово - "
                             "Перевод</code>\n\nКаждая пара слов должна начинаться с новой строки:\n\n<code>Слово - "
                             "Перевод</code>\n<code>Слово - Перевод</code>", parse_mode='HTML')
        return
    msg_text_list_words = message.text.replace(' - ', ' ').split()
    lol = lambda lst, sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]
    msg_text_list_words = lol(msg_text_list_words, 2)
    msg_text_list_words = dict(msg_text_list_words)

    for word, translate in msg_text_list_words.items():
        if await db.async_get_word(word=word.capitalize()):
            added_words += word + ', '
            continue
        data = await state.get_data()
        category = data.get('category')
        await db.async_add_new_word(category=category, word=word.capitalize(), translate=translate.capitalize(),
                                    user_id=message.from_user.id)

    if not added_words:
        await message.answer("Слово(-а) успешно добавлено(-ы)!", reply_markup=kb.kbStart)
    else:
        await message.answer(f"Не все слова были добавлены.\n\n"
                             f"Слова, которые уже были в таблице и не были добавлены: {added_words}")
    await state.finish()


@dp.message_handler(commands=['testing'])
@dp.message_handler(lambda msg: msg.text.lower()[:-2] == 'тестирование')
async def testing_select_category(message: types.Message):
    await message.answer("Вы перешли в меню тестирования", reply_markup=ReplyKeyboardRemove())
    await message.answer("Пожалуйста, выберите категорию, по которой будет проводиться тест.",
                         reply_markup=kb.categories_with_all)
    await Testing.waiting_for_choose_category.set()


@dp.callback_query_handler(state=Testing.waiting_for_choose_category)
async def testing_select_difficult(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=call.data)

    await call.message.answer("Пожалуйста, выберите сложность теста.\n<b>Лёгкий</b> - вам будут даны четыре варианта "
                              "ответа, из которых нужно будет выбрать один верный\n<b>Продвинутый</b> - перевод для "
                              "слова "
                              "нужно написать самостоятельно", reply_markup=kb.kbChooseDifficult, parse_mode='HTML')

    await Testing.difficult_selected.set()


@dp.callback_query_handler(text_contains='easy', state=Testing.difficult_selected)
async def testing_easy_difficult(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(current_difficult='easy')

    import random
    data = await state.get_data()
    i = 0
    answers = {}

    kbAnswersChoose = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    category = data.get("category")
    words = await db.async_testing_easy_difficult(category=category)

    for word in words:
        answers[i] = word[0][1]
        i += 1
    for button_name, word in answers.items():
        button_name = KeyboardButton(word)
        kbAnswersChoose.insert(button_name)
    btnGoBack = KeyboardButton("Вернуться в главное меню")
    kbAnswersChoose.insert(btnGoBack)

    word_and_translate = random.choice(words[random.randint(0, 3)])
    word_originally = word_and_translate[0]
    word_translate = word_and_translate[1]

    await state.update_data(word_translate=word_translate)

    await call.message.answer(f"Дано слово: {word_originally}\n\nКаков его перевод?",
                              reply_markup=kbAnswersChoose)

    await Testing.waiting_for_choose_right_answer.set()


@dp.message_handler(state=Testing.waiting_for_choose_right_answer)
async def testing_answer(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)

    data = await state.get_data()
    current_difficult = data.get('current_difficult')

    if current_difficult == 'easy':
        btnAgain = InlineKeyboardButton("Ещё слово", callback_data='easy')
    else:
        btnAgain = InlineKeyboardButton("Ещё слово", callback_data='hard')
    btnBack = InlineKeyboardButton("Вернуться назад", callback_data='back')
    kbAgainOrBack = InlineKeyboardMarkup(row_width=1)
    kbAgainOrBack.insert(btnAgain)
    kbAgainOrBack.insert(btnBack)

    if data.get('answer') == data.get('word_translate'):
        await message.answer(f"Верно! Это слово переводится, как {data.get('answer')}!", reply_markup=kbAgainOrBack)
    else:
        await message.answer(f"К сожалению, ты ошибься. Это слово переводится, как {data.get('word_translate')}. Будь "
                             f"внимательнее в следующий раз!", reply_markup=kbAgainOrBack)

    await Testing.difficult_selected.set()


@dp.callback_query_handler(text_contains='hard', state=Testing.difficult_selected)
async def testing_hard_difficult(call: types.CallbackQuery, state: FSMContext):
    import random

    await state.update_data(current_difficult='hard')

    data = await state.get_data()
    category = data.get('category')

    word_and_translate = await db.async_testing_hard_difficult(category=category)

    word = word_and_translate[0]
    translate = word_and_translate[1]

    if random.randint(0, 1) == 1:
        word, translate = translate, word

    await state.update_data(word_translate=translate)

    await call.message.answer(f"Дано слово: {word}\n\nКаков его перевод?")

    await Testing.waiting_for_choose_right_answer.set()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Я не знаю такой команды :(\nВведи /help, чтобы посмотреть список возможных команд или "
                         "воспользуйся меню.")
    print(demojize(message.text.lower()) == 'тестирование')
