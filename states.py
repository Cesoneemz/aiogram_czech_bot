from aiogram.dispatcher.filters.state import State, StatesGroup


class AddWord(StatesGroup):
    waiting_for_category = State()
    waiting_for_word = State()
    write_to_database = State()


class Testing(StatesGroup):
    waiting_for_choose_category = State()
    waiting_for_choose_difficult = State()
    difficult_selected = State()
    waiting_for_choose_right_answer = State()
