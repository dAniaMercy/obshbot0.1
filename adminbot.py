# coding: utf-8
import sqlite3
import telebot
from telebot import types # для указание типов
import datetime
import ded

token1 = '6345762065:AAGNpWtnBIvQ9Sua3-Jj1m_krDrkckHnUbw'
bot1=telebot.TeleBot(token1)

conn = sqlite3.connect('admin.db', check_same_thread=False)
cursor = conn.cursor()

ded.tcheckconnectt()
log = input()
passs = input()

cursor.execute('''SELECT * FROM admincheck WHERE login = ?''', log)
print(cursor.fetchall())

row = cursor.fetchone()
if row[3] > 0:
  
    print('trying register, id:')
else:
   print('login or password are false')







if log == row[1] and passs == row[2]:
    cursor.close()
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()

    dt_now = datetime.datetime.now()
    print(dt_now,'>>> bot-started')



    @bot1.message_handler(commands=['start'])
    def start_message(message):
        bot1.send_message(message.chat.id, 'Добро пожаловать ✋ \nЧтобы узнать команды, поддерживаемые бота 📕 \nнапиши /help')



    @bot1.message_handler(commands=['all'])
    def start_message(message):
        cdt=datetime.datetime.now()
        cdt=str(cdt)
        cursor = conn.execute("select * from test")
        
        print('\nUser:', "@",str(message.from_user.username), 'command: ',{str(message.text)}, '\ntime:', dt_now,'\n')
        data=cursor.execute('''SELECT * FROM test''')
        for row in data:
            print(row)



    bot1.infinity_polling(none_stop=True)