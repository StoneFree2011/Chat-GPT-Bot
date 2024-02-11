import tokens #удалите строку, если не используете отдельный tokens.py

bot_token=tokens.token #'токен бота' (str)

admin_id=tokens.admins_id #Кто будет администрировать бота (int)

browser_xy=tokens.browser_xy #Координаты браузера на панели задач [x, y]

enter_xy=tokens.enter_xy #Координаты строки запроса на сайте [x, y]

answer_xy=tokens.answer_xy #Координаты кнопки копирования ответа [x, y]
#(ВНИМАНИЕ: !Чат не должен быть пустым, это координаты при условии, что кнопка находится в максимально возможном низком положении)

pagedown_xy=tokens.pagedown_xy #Координаты кнопки стрелочки вниз [x, y]

#координаты можно определить с помощью следующего скрипта (расскоментируйте и запустите settings.py несколько раз для каждого пункта):
"""
from time import sleep
from pyautogui import position

def find_coordinates(time):
    sleep(time) #задержка, чтобы вы успели переместить мышку в нужное место
    return(position()) #координаты выведутся в консоль и вы сможете их вбить
    
print(find_coordinates(6)) #6 секунд задержки перед срабатыванием
"""