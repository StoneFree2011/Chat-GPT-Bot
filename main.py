from Chat_GPT_BOT import *

try:
    time.sleep(3)
    pyautogui.click(360, 1054) #корды браузера
    time.sleep(1)
    pyautogui.click(680, 957) #корды строки
    bot_online()
    threading.Thread(target=process_messages, daemon=True).start()   # Запуск потока для обработки сообщений из очереди
    bot.polling(none_stop=True) # Запуск бота
finally: #на случай аварийного завершения работы
    bot_offline()