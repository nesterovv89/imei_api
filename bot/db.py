import logging

import aiosqlite
from sqlalchemy import Column, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
logging.basicConfig(level=logging.INFO)



class Profile(Base):
    __tablename__ = 'profile'

    user_id = Column(String, primary_key=True)


async def create_tables():
    async with aiosqlite.connect('bot.sqlite3') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                user_id TEXT PRIMARY KEY
            )
        """)
        await db.commit()


async def is_user_whitelisted(user_id):
    """Проверка есть ли пользователь в БД"""
    engine = create_async_engine('sqlite+aiosqlite:///bot.sqlite3')
    async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        result = await session.execute(select(Profile).where(Profile.user_id == user_id))
        return result.scalars().first() is not None
    

async def add_user_to_whitelist(user_id):
    """Добавление пользователя в БД"""
    engine = create_async_engine('sqlite+aiosqlite:///bot.sqlite3')
    async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        session.add(Profile(user_id=user_id))
        await session.commit()
