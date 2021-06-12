# Импорты
import telebot
import config
import sqlite3
import time

bot = telebot.TeleBot(config.token)
print("Запущен в работу")
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/bold', '/not_bold')
    keyboard.row('/fat', '/not_fat')
    keyboard.row('/show_statistics')

    bot.send_message(message.chat.id, "Увидел чела на Камри? Посмотри - лысый ли он!\n"
                                      "Если лысый - напиши /bold\nЕсли нет - /not_bold\n"
                                      "Если толстый - напиши /fat\nЕсли нет - /not_fat\n"
                                      "Хочешь посмотреть статистику? Жми - /show_statistics\n",
                                       reply_markup=keyboard)



@bot.message_handler(commands=['show_db'])
def show_db(message):
    # Подключение или создание БДы
    con = sqlite3.connect("Tasks.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS nic (id INTEGER PRIMARY KEY, p1 TEXT, p2 TEXT, p3 TEXT)")
    # Выгрузка и формирование списка БДы
    new = []
    for i in cur.execute("SELECT * FROM nic"):
        i = str("{}. {}, {}".format(i[0], i[1], i[2]))
        new.append(i)
    # Форматирование списка для вывода
    sp = '\n'.join(new)
    # Дроп базы
    con.commit()
    cur.close()
    con.close()
    try:
        bot.send_message(message.chat.id, sp, None)
    except:
        bot.send_message(message.chat.id, 'База данных пуста!', None)

# Блок бота на добавление лысых
@bot.message_handler(commands=['bold'])
def bold(message):
    answer = 'bold'
    con = sqlite3.connect("Tasks.db")
    cur = con.cursor()
    cur.execute("INSERT INTO nic(id,p1,p2) VALUES(NULL, %r,NULL)" % answer)
    con.commit()
    cur.close()
    con.close()
    bot.send_message(message.chat.id, config.show_text('bold'), None)
    print(time.ctime(), "id - ", message.chat.username, '- added \"bold\"')


# Блок бота на добавление волосатых
@bot.message_handler(commands=['not_bold'])
def not_bold(message):
    answer = 'notbold'
    con = sqlite3.connect("Tasks.db")
    cur = con.cursor()
    cur.execute("INSERT INTO nic(id,p1,p2) VALUES(NULL, %r,NULL)" % answer)
    con.commit()
    cur.close()
    con.close()
    bot.send_message(message.chat.id, config.show_text('not_bold'), None)
    print(time.ctime(), "id - ", message.chat.username, '- added \"not_bold\"')

# Блок бота на добавление Толстых
@bot.message_handler(commands=['fat'])
def fat(message):
    answer = 'fat'
    con = sqlite3.connect("Tasks.db")
    cur = con.cursor()
    cur.execute("INSERT INTO nic(id,p1, p2) VALUES(NULL,NULL, %r)" % answer)
    con.commit()
    cur.close()
    con.close()
    bot.send_message(message.chat.id, config.show_text('fat'), None)
    print(time.ctime(), "id - ", message.chat.username, '- added \"fat\"')


# Блок бота на добавление Худых
@bot.message_handler(commands=['not_fat'])
def not_fat(message):
    answer = 'notfat'
    con = sqlite3.connect("Tasks.db")
    cur = con.cursor()
    cur.execute("INSERT INTO nic(id,p1, p2) VALUES(NULL,NULL, %r)" % answer)
    con.commit()
    cur.close()
    con.close()
    bot.send_message(message.chat.id, config.show_text('not_fat'), None)
    print(time.ctime(), "id - ", message.chat.username, '- added \"not_fat\"')

@bot.message_handler(commands=['show_statistics'])
def show_statistics(message):
    con = sqlite3.connect("Tasks.db")
    cur = con.cursor()
    # Смотрим общее количество записей
    for i in cur.execute("SELECT COUNT(1) FROM nic"):
        all_count = i

    # Смотрим общее количество лысых
    for i in cur.execute("SELECT COUNT(*) FROM nic WHERE p1='bold'"):
        bold_count = i
    for i in cur.execute("SELECT COUNT(*) FROM nic WHERE p1='notbold'"):
        not_bold_count = i

    for i in cur.execute("SELECT COUNT(*) FROM nic WHERE p2='fat'"):
        fat_count = i
    for i in cur.execute("SELECT COUNT(*) FROM nic WHERE p2='notfat'"):
        not_fat_count = i

    all_count, bold_count, not_bold_count, fat_count, not_fat_count = all_count[0], bold_count[0], not_bold_count[0], fat_count[0], not_fat_count[0]
    all_for_bald = bold_count + not_bold_count
    all_for_fat = fat_count + not_fat_count

    bold_perc, not_bold_perc = float(bold_count) / float(all_for_bald), float(not_bold_count) / float(all_for_bald)
    fat_perc, not_fat_perc = float(fat_count) / float(all_for_fat), float(not_fat_count) / float(all_for_fat)
    output = "Всего записей в базе - {} .\nИз них:\nлысых - {:.2%}, волосатых - {:.2%}\nтолстых - {:.2%}, худых - {:.2%}"\
        .format(all_count, bold_perc, not_bold_perc, fat_perc, not_fat_perc)
    con.commit()
    cur.close()
    con.close()
    bot.send_message(message.chat.id, output, None)

@bot.message_handler(commands=['delete_db'])
def delete_db(message):
    con = sqlite3.connect("Tasks.db")
    cur = con.cursor()
    cur.execute("DELETE FROM nic")
    con.commit()
    cur.close()
    con.close()
    bot.send_message(message.chat.id, 'deleted')
    print('База данных очищена пользователем -', message.chat.username)

if __name__ == '__main__':
    bot.polling(none_stop=True)