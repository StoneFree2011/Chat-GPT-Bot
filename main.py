from Chat_GPT_BOT import *

try:
    time.sleep(1)
    pyautogui.click(browser_xy) #корды браузера
    time.sleep(5)
    pyautogui.click(enter_xy) #корды строки запроса
    bot_online()
    threading.Thread(target=process_messages, daemon=True).start()   # Запуск потока для обработки сообщений из очереди
    bot.polling(none_stop=True) # Запуск бота
finally: #на случай аварийного завершения работы
    bot_offline()