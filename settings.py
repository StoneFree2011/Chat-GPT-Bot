from tokens import test_token, token, admins_id #удалите строку, если нет отдельного tokens.py

bot_token=token #'токен бота' (str)

admin_id=admins_id #user_id (кто будет администрировать бота) (int)

browser_xy=[378, 1052] #Координаты браузера на панели задач [x, y]

enter_xy=[731, 936] #Координаты строки запроса на сайте [x, y]:

answer_xy=[678, 811] #Координаты кнопки копирования ответа [x, y] (в строке запроса должно быть пусто):

#координаты можно определить с помощью следующего скрипта:
"""
from time import sleep
from pyautogui import position

def find_coordinates(time):
    sleep(time) #задержка, чтобы вы успели переместить мышку в нужное место
    return(position()) #координаты выведутся в консоль и вы сможете их вбить
    
print(find_coordinates(6)) #6 секунд задержки перед срабатыванием
"""
