from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import random

bot = Bot(token='Your_bot_token')
dp = Dispatcher(bot)

participants = {}
banned_users = set()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = '''/Привіт, це бот для розіграшу 2000 в-баксів! Щоб прийняти участь, напиши мені команду /add і свій нік в грі Fortnite, а я рандомним чином виберу переможця.
    Зверни увагу, що переписати нікнейм повторно не можливо, тому постарайся написати без помилок з 1 разу!'''
    await message.reply(text)

@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    if message.from_user.id in banned_users:
        return  # Якщо користувач заборонений, ігноруємо повідомлення

    if len(message.text.split()) > 1:
        nickname = " ".join(message.text.split()[1:])
        participants[message.from_user.id] = nickname
        text = "Тепер ти береш участь у розіграші. Змінити нікнейм більше не можливо."
        banned_users.add(message.from_user.id)  # Додаємо користувача до списку заборонених
    else:
        text = "Некоректний формат команди. Введи /add [тут будь які символи]."
    await message.reply(text)

@dp.message_handler(commands=['result'])
async def result(message: types.Message):
    if participants:
        winner_id = random.choice(list(participants.keys()))
        winner_nickname = participants[winner_id]
        text = f"Переможець розіграшу: {winner_nickname}"
    else:
        text = "Немає учасників у розіграші."
    await message.reply(text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
