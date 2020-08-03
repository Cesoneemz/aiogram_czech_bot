from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import emoji

btnHelp = KeyboardButton(emoji.emojize(':warning:') + "Помощь" + emoji.emojize(':warning:'))
btnTest = KeyboardButton("Тестирование " + emoji.emojize(':pencil:'))
btnAddWord = KeyboardButton("Добавить слово " + emoji.emojize(':envelope:'))
kbStart = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTest, btnAddWord).add(btnHelp)

btnEasy = InlineKeyboardButton("Лёгкий", callback_data='easy')
btnHard = InlineKeyboardButton("Продвинутый", callback_data='hard')
btnBack = InlineKeyboardButton("Вернуться в главное меню", callback_data='back')
kbChooseDifficult = InlineKeyboardMarkup(row_width=2)
kbChooseDifficult.add(btnEasy, btnHard, btnBack)

btnForward = KeyboardButton("Ещё слово")
kbForwardOrBack = ReplyKeyboardMarkup(resize_keyboard=True).add(btnForward, btnBack)

categories = InlineKeyboardMarkup(row_width=3)
categories_with_all = InlineKeyboardMarkup(row_width=3)

btnCategoriesFamily = InlineKeyboardButton(text="Семья" + emoji.emojize(':family:'), callback_data="family")
categories.insert(btnCategoriesFamily)
categories_with_all.insert(btnCategoriesFamily)

btnCategoriesAnimal = InlineKeyboardButton(text="Животные" + emoji.emojize(':snake:'), callback_data="animal")
categories.insert(btnCategoriesAnimal)
categories_with_all.insert(btnCategoriesAnimal)

btnCategoriesNature = InlineKeyboardButton(text="Природа" + emoji.emojize(':sun:'), callback_data="nature")
categories_with_all.insert(btnCategoriesNature)

btnCateroriesAll = InlineKeyboardButton('Всё', callback_data='all')
categories_with_all.insert(btnCateroriesAll)

btnCategoriesBack = InlineKeyboardButton(text="Назад", callback_data="back")
categories_with_all.insert(btnCategoriesBack)


btnBan = KeyboardButton("Забанить пользователя")
btnUnBan = KeyboardButton("Разбанить пользователя")
btnAllWords = KeyboardButton("Прислать все слова, с ID")
btnDeleteWord = KeyboardButton("Удалить слово по ID")
btnEditWord = KeyboardButton("Исправить слово по ID")
btnLogout = KeyboardButton("Выйти из админ-панели")
adminKeyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True).add(btnBan, btnUnBan, btnAllWords, btnDeleteWord,
                                                                           btnEditWord, btnLogout)
