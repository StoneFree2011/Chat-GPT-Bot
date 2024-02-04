import pyautogui
import pyperclip
import telebot
import threading
import queue
import time
import atexit
import sqlite3
import os
from tokens import token, admin_id, test_token


bot = telebot.TeleBot(test_token) #токен хранится в tokens.py
message_queue = queue.Queue() #очередь сообщений
    
def bot_online():
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, history TEXT)""")
    connect.commit()
    try:
        all_results = []
        for i in cursor.execute("SELECT id FROM users"):
            all_results += i
        connect.commit()
        for i in range(0, len(all_results)):
            bot.send_message(chat_id = all_results[i], text = '🤖 Мои мыслительные процессы запущены')
    except Exception as e:
        bot.send_message(chat_id = admin_id, text = '❌ Ошибка запуска'+repr(e))


def process_messages():
    while True:
        message = message_queue.get()
        timing = time.time() #таймер зависаний
        pyperclip.copy(message.text)
        answer = bot.send_message(message.chat.id, 'Обработка запроса🧑‍🦼', reply_to_message_id=message.message_id, parse_mode='Markdown')
        pyautogui.hotkey('ctrl', 'v') #чтоб это работало ОБЯЗАТЕЛЬНА английская расскладка
        time.sleep(0.1)
        pyautogui.hotkey('enter')
        while pyperclip.paste() == message.text:
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(2)
            pyautogui.hotkey('pagedown') #пролистывание строки вниз (на случай, когда текста много)
            pyautogui.click(683, 851) #корды копирования ответа
            if time.time() - timing > 40.0:
                timing = time.time()
                bot.send_message(chat_id = admin_id, text = 'У нас проблемы, босс')
        time.sleep(1)
        bot.edit_message_text(chat_id = message.chat.id, message_id = answer.message_id, text = pyperclip.paste(), parse_mode='Markdown')
        pyautogui.click(680, 957) #корды строки
        
        try:
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
            if cursor.fetchone() is None: #проверка, что юзер уже есть в базе
                cursor.execute(f"""INSERT INTO users (id, username, history) 
                               VALUES ('{message.from_user.id}', '{message.from_user.username}', 'Начало диалога: ')""") #добавить, если нет
                connect.commit()
            else:
                cursor.execute(f"UPDATE users SET username = '{message.from_user.username}' WHERE id = '{message.from_user.id}'") #обновить юзернейм, если есть
                connect.commit()
            cursor.execute(f"SELECT history FROM users WHERE id = '{message.from_user.id}'")
            i = cursor.fetchone() #старая история
            date_format='%d.%m.%Y %H:%M:%S'
            cursor.execute(f"""UPDATE users SET history = '{i[0]}\n🗣{time.strftime(date_format, time.localtime())}
                           -{message.text}\n🤖 -{pyperclip.paste()}' WHERE id='{message.from_user.id}'""")
            connect.commit() #в базу занесся диалог
            connect.close()
        except Exception as e:
            bot.send_message(chat_id = admin_id, text = 'Ошибка занесения в базу: ' + repr(e)) #отправить ошибку админу
        message_queue.task_done()

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"""ℹ️Пожалуйста, не спамьте множеством сообщений. Это замедляет генерацию ответов как для вас, так и для других пользователей.
                     \nЕсли бот долго не отвечает на ваше сообщение, значит очередь слишком большая. *Не надо спамить!* 
                     \n\nℹ️__Некоторые советы и информацию о боте можно узнать по команде__ /help 
                     \n\n🤖А теперь, задавайте ваш вопрос!""", parse_mode='Markdown')
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
    if cursor.fetchone() is None: #проверка, что юзер уже есть в базе
        cursor.execute(f"""INSERT INTO users (id, username, history) 
                       VALUES ('{message.from_user.id}', '{message.from_user.username}', 'Начало диалога:')""") #добавить, если нет
    else:
        cursor.execute(f"UPDATE users SET username = '{message.from_user.username}' WHERE id = '{message.from_user.id}'") #обновить юзернейм, если есть
    connect.commit()
    connect.close()

@bot.message_handler(commands=['stop']) #остановка работы бота (только для админа)
def stop(message):
    if message.from_user.id == admin_id:
        bot_offline()
    else:
        bot.send_message(message.chat.id, 'КТО ты такой, чтобы меня останавливать?😁')
 
@bot.message_handler(commands=['help'], content_types=['text'])
def help(message):
    if message.from_user.id != admin_id:
        command, _, text_after_command = message.text.partition(' ')
        if command == '/help' and text_after_command: #если указано сообщение
            bot.send_message(chat_id = admin_id, text = f"@{message.from_user.username} передал:\n{text_after_command}")
            bot.send_message(message.chat.id,'Я передал вашу кляузу начальству')
        else:
            bot.send_message(message.chat.id, f"""ℹ️*Советы:*\nЕсли бот долго не отвечает на ваше сообщение, значит очередь слишком большая (либо он сдох). *Не надо спамить!*
                             \n\nПри запросе математических рассчетов добавляйте _Сделай это в разметке для Телеграм_
                             \nВ противном случае ответ может быть *не читаемым*.\nПример: (пока что его нет ахпхахп)""", parse_mode='Markdown')
            bot.send_message(message.chat.id, f"""🌐 [Репозиторий бота на GitHub](https://github.com/StoneFree2011/Chat-GPT-Bot)
                             \n\nЕсли хотите сообщить об ошибке или передать пару ласковых админу, то используйте команду:
                             \n/help `Ваше сообщение`""", parse_mode='Markdown')
    else:
        command, _, text_after_command = message.text.partition('@')
        username, _, text = text_after_command.partition(' ')
        try:
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute(f"SELECT id FROM users WHERE username = '{username}'")
            i = cursor.fetchone()
            bot.send_message(chat_id = i[0], text = text) #отправить ответ пользователю
            connect.commit()
            connect.close()
        except Exception as e:
            bot.send_message(message.chat.id, '❌ Ошибка ответа '+repr(e))
         

@bot.message_handler(commands=['log'], content_types=['text'])
def log(message): #логи переписок пользователей
    if message.from_user.id == admin_id: #доступ к команде только у админа
        command, _, text_after_command = message.text.partition('@')
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        try:
            if command == '/log' and text_after_command: #если указан юзернейм пользователя вывести его историю
                cursor.execute(f"SELECT history FROM users WHERE username = '{text_after_command}'")
                logs= cursor.fetchone()
                for i in range(0, len(logs[0]), 1000): #учитываем макс длину сообщения телеграм (1024, но взял с запасом)
                    bot.send_message(message.chat.id, logs[0][i:i+1000], parse_mode='Markdown')
            else: #если команда /log без юзернейма, вывести юзернеймы всех пользователей
                 cursor.execute("SELECT username FROM users")
                 usernames=cursor.fetchall()
                 logs = "\n@".join(i[0] for i in usernames)
                 bot.send_message(message.chat.id, text=f"Все пользователи бота:\n@{logs}")
            connect.commit()
            connect.close()
        except Exception as e:
            bot.send_message(message.chat.id, '❌ Ошибка логирования '+repr(e))
    else:
        bot.send_message(message.chat.id, 'Это не для тебя было сделано и не для таких, как ты')
        
@bot.message_handler(commands=['wipe'], content_types=['text']) 
def wipe(message): #вайп истории
    if message.from_user.id == admin_id:
        command, _, text_after_command = message.text.partition('@')
        if command == '/wipe' and text_after_command:
            # Выполняем команду с текстом
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            try:
                cursor.execute(f"UPDATE users SET history = 'Начало диалога: ' WHERE username = '{text_after_command}'")
                connect.commit()
                connect.close()
            except Exception as e:
                bot.send_message(message.chat.id, '❌ Ошибка вайпа '+repr(e))
        else:
            bot.send_message(message.chat.id, "Неправильное использование команды /wipe\nВведите @username сразу после команды (без пробела)")
    else:
        bot.send_message(message.chat.id, 'Это не для тебя было сделано и не для таких, как ты')
    
@bot.message_handler(content_types=['text'])
def talk(message):
    message_queue.put(message)

@atexit.register
def bot_offline(): #скрипт завершения программы
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    connect.commit()
    try:
        all_results = []
        for i in cursor.execute("SELECT id FROM users"):
            all_results += i
        connect.commit()
        for i in range(0, len(all_results)):
            bot.send_message(chat_id = all_results[i], text = '🛏 Я пошел на подзарядку, что либо писать бессмысленно. Мне плевать.')
    except Exception as e:
        bot.send_message(chat_id = admin_id, text = '❌ Ошибка выключения')
    cursor.close()
    connect.close()
    #sys.exit() # завершаем программу (почему-то не работает, скорее всего из-за многопоточности)
    os._exit(0) # завершаем программу