from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import re

from keyboards import kb_whois, inline_kb_whois

import whois

import os

bot = Bot(token = os.getenv('TOKEN'))
dp = Dispatcher(bot)

async def startup_on(_):
    print('Бот в вышел в онлайн')

@dp.message_handler(commands='start')
@dp.message_handler(regexp='\s*@torrentxok_testbot\s*/start\s*')
async def command_start(message : types.Message):
    try:
        start_message ='''
Привет)
Это бот, который отправляет Whois-запросы

Он позволяет отслеживать домены, которые вы добавите,
и выводить информацию о домене!

Обновление информации добавленных доменов происходит один раз в день

Также возможно настроить систему оповещений

Инструкцию по командам, которые есть у бота, \
можно просмотреть по запросу:
/help

Список команд доступен по запросу:
/commands'''
        await bot.send_message(message.from_user.id, start_message, reply_markup=kb_whois)
    
    except:
        await message.reply(f'Ошибка! Напишите боту (@{(await bot.get_me()).username}) в личные сообщения')

@dp.message_handler(commands='help')
@dp.message_handler(regexp='\s*@torrentxok_testbot\s*/help\s*')
async def command_list(message : types.Message):
    try:
        help_message = '''
Доступные команды :

/commands - просмотреть список доступных запросов

Шаблоны:

/find     { your domain } - Выполняет whois-запрос и выводит информацию о домене

/add    { your domain } - Добавляет домен для отслеживания

/delete    { your domain } - Удаляет ранее добавленный домен

/list - Просмотр добавленных доменов

Вместо { your domain } вставьте имя домена, который хотите проверить
(без {} и без http)'''
        await bot.send_message(message.from_user.id, help_message, reply_markup=kb_whois)
    except:
        await message.reply('Общение с ботом в ЛС!')

@dp.message_handler(commands='commands')
@dp.message_handler(regexp='\s*@torrentxok_testbot\s*/commands\s*')
async def command_whois(message : types.Message):
    commands_message = '''
Инструкция по доступным командым:
/help

Команды: '''
    await bot.send_message(message.from_user.id, commands_message, reply_markup=inline_kb_whois)


    #await message.reply(message.text)
@dp.message_handler(regexp='\s*@torrentxok_testbot\s*/find\s*\w*\s*') 
@dp.message_handler(regexp='\s*/find\s*\w*\s*')
async def find_domain(message : types.Message):
    domain_name = message.text[message.text.find('find')+4:].strip()
    if len(domain_name.split())!=1:
        await bot.send_message(message.from_user.id, 'Неверное имя домена!\nИнструкция по использованию бота:\n/help')
    else:
        try:
            #информация о домене
            whois_find_domain = whois.whois(domain_name)
            print(whois_find_domain)
            if type(whois_find_domain['creation_date']) == list:
                creation_date = str(whois_find_domain['creation_date'][1])[:11].strip().split('-')
            elif type(whois_find_domain['creation_date']) == datetime:
                creation_date = str(whois_find_domain['creation_date'])[:11].strip().split('-')
            creation_date_year = creation_date[0]
            creation_date_month = creation_date[1]
            creation_date_day = creation_date[2]

            if type(whois_find_domain['expiration_date']) == list:
                expiration_date = str(whois_find_domain['expiration_date'][1])[:11].strip().split('-')
            elif type(whois_find_domain['expiration_date']) == datetime:
                expiration_date = str(whois_find_domain['expiration_date'])[:11].strip().split('-')
            expiration_date_year = expiration_date[0]
            expiration_date_month = expiration_date[1]
            expiration_date_day = expiration_date[2]

            whois_info = f'''
Domain : {whois_find_domain['domain_name']}
Creation date : {creation_date_day}.{creation_date_month}.{creation_date_year}
Expiration date : {expiration_date_day}.{expiration_date_month}.{expiration_date_year}
'''
            await bot.send_message(message.from_user.id, whois_info)
        except:
            await bot.send_message(message.from_user.id, 'Произошла ошибка!\nПопробуйте еще раз или введите другое имя домена\n\nИнструкция доступна по запросу:\n/help' )


executor.start_polling(dp, skip_updates=True, on_startup=startup_on)