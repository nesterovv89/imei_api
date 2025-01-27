from aiogram.fsm.state import State, StatesGroup


class Imei(StatesGroup):

    imei = State()
    service_id = State()
