from aiogram.filters.state import State, StatesGroup


class SetConfig(StatesGroup):
    cf_choosing_from_channel = State()
    cf_choosing_to_channel = State()
    cf_filter_in = State()
    cf_filter_out = State()
