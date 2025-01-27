import re

from aiogram import types
from aiogram.filters import Filter


class ImeiFilter(Filter):
    """ Фильтр для валидации IMEI """
    async def __call__(self, message: types.Message) -> bool:
        if message.text:
            return bool(re.match(r'^\d{8,15}$', message.text))
        return False
    

def format_response(data, indent=0):
    """Функция для форматирования ответа"""
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f'{'  ' * indent}{key}:')
            lines.extend(format_response(value, indent + 1))
        else:
            lines.append(f'{'  ' * indent}{key}: {value}')
    return lines


async def fetch(session, url, data=None, method='GET', headers=None):
    """Функция для выполнения асинхронного запроса"""
    async with session.request(method, url, params=data, headers=headers) as response:
        response.raise_for_status()
        return await response.json()
