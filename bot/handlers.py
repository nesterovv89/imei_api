import logging
import os

from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientSession
from dotenv import load_dotenv

from api.schemas import ServiceItem

from . import keyboards as k
from .db import add_user_to_whitelist, is_user_whitelisted
from .states import Imei
from .utils import ImeiFilter, format_response, fetch

logging.basicConfig(level=logging.INFO)

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
BACKEND_API_URL = os.getenv('BACKEND_URL')
API_KEY = os.getenv('COMMON_TOKEN')

bot = Bot(token=TELEGRAM_BOT_TOKEN)
router = Router()


@router.message(Command('start'))
async def start(message: types.Message):
    """Обработка старта"""
    if await is_user_whitelisted(user_id=message.from_user.id):
        await message.answer(
            text='Вы есть в списке пользователей, приятной работы.',
            reply_markup=k.keyboard
        )
    else:
        await message.answer(text='Вас нет в списке пользователей, добавиться '
                             'в список для тестового использования можно по кнопке ниже:',
                             reply_markup=k.keyboard_2)


@router.callback_query(F.data == 'test')
async def approved_start(callback: types.CallbackQuery):
    """Кнопка добавления в БД на тест"""
    await add_user_to_whitelist(user_id=callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        text=f'{callback.from_user.full_name}, Вы успешно добавлены в whitelist, функционал доступен:', reply_markup=k.keyboard
    )


@router.callback_query(F.data == 'get')
async def get_services(callback: types.CallbackQuery, state: FSMContext):
    """Запрос IMEI"""
    await callback.message.answer(
            text='Введите IMEI:')
    await state.set_state(Imei.imei)


@router.message(ImeiFilter(), Imei.imei)
async def handle_imei(message: types.Message, state: FSMContext):
    """ООбработка IMEI, получение списка услуг"""
    imei = message.text.lower()
    headers = {'X-API-Key': API_KEY}
    params = {'imei': imei}

    async with ClientSession() as session:

        response = await fetch(
            session, f'{BACKEND_API_URL}/api/check-imei', data=params, method='POST', headers=headers
        )
        services = [ServiceItem(**item) for item in response['services']]
        balance = response['balance']
        formatted_services = []
        builder = InlineKeyboardBuilder()
        try:
            for service in services:
                formatted_services.append(
                    f'{service.id}. {service.title}. Price = {service.price} USD'
                )
                builder.button(
                    text=f'Купить {service.title}', callback_data=f'buy_{service.id}'
                )
            builder.adjust(1)
            message_text = (
                            f'Доступные услуги для IMEI: {imei}\n'
                            f'Ваш баланс: {balance} USD\n'
                            f'Список услуг:\n'
                            f'{chr(10).join(formatted_services)}\n'
                            )
            await message.answer(
                message_text, reply_markup=builder.as_markup()
            )
            await state.update_data(imei=imei)
            await state.set_state(Imei.service_id)
        except Exception as e:
            await message.answer(f'Ошибка: {e}')


@router.message(Imei.imei)
async def handle_invalid_imei(message: types.Message):
    await message.answer(
        'Неверный формат IMEI. IMEI должен содержать от 8 до 15 цифр.'
    )


@router.callback_query(F.data.startswith('buy_'), Imei.service_id)
async def buy_service(callback: types.CallbackQuery, state: FSMContext):
    """Получение услуги"""
    data = await state.get_data()
    imei = data['imei']
    service_id = int(callback.data.split('_')[1])
    headers = {'X-API-Key': API_KEY}
    params = {'imei': imei, 'service_id': service_id}
    async with ClientSession() as session:
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
            response = await fetch(
                session, f'{BACKEND_API_URL}/api/purchase', data=params,
                method='POST', headers=headers
            )
            formatted_response = '\n'.join(format_response(response))
            await callback.message.answer(
                f'Результат покупки:\n{formatted_response}'
            )
        except Exception as e:
            await callback.message.answer(f'Ошибка при покупке: {e}')
        finally:
            await state.clear()
            await callback.message.answer(
                text='Введите новый IMEI', reply_markup=k.keyboard
            )
