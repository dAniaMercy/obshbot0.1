# coding: utf-8
from email.message import Message
import sqlite3
from xml.sax.handler import DTDHandler
import telebot
from telebot import types # для указание типов
import datetime
import ded
import base64
from pathlib import Path


token = '6204506293:AAE4S02ArqABxDKu7WiUIZBjtyNWaOIgLC8'
bot=telebot.TeleBot(token)




dt_now = datetime.datetime.now()
print(dt_now,'>>> bot-started')

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


ded.checkconnect()





@bot.message_handler(commands=['addmyprof'])
def start_message(message):
	
	us_id = message.from_user.id
	us_nam = message.from_user.first_name
	username = message.from_user.username
	dt_now = datetime.datetime.now()
	dr = dt_now 
	cursor = conn.execute("SELECT COUNT(*) from test WHERE user_id = ?", (message.from_user.id,))
	row = cursor.fetchone()
	if row[0] > 0:
		bot.send_message(message.chat.id, 'Ты уже зарегистрирован')
		print(dt_now, 'trying register, id:', us_id, 'name:', us_nam)
	else:
		print(dt_now, "not found, reg", us_id, ",", username, ",", us_nam)
		ded.db_table_val(user_id=us_id, user_name=us_nam, username=username, datareg = dr)
		bot.send_message(message.chat.id, 'Привет! Ваше имя добавлено в базу данных!')



@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Добро пожаловать ✋ \nЧтобы узнать команды, поддерживаемые бота 📕 \nнапиши /help')




@bot.message_handler(commands=['help'])
def start_message(message):
    cdt=datetime.datetime.now()
    cdt=str(cdt)
    bot.send_message(message.chat.id, f'Привет, {str(message.chat.first_name)}! \nСпасибо за обращению в службу _test_ \n Чтобы зарегистрировать себя используй команду /addmyprof \n Чтобы прислать улику /report')
    print('\nUser:', "@",str(message.from_user.username), 'command: ',{str(message.text)}, '\ntime:', dt_now )

@bot.message_handler(commands=['report'])
def get_text_messages(message):
	bot.send_message(message.chat.id, 'Проверка пользователя, подождите...')
	#bot.send_message(message.chat.id, message.text)
	dt_now = datetime.datetime.now()
	us_id = message.from_user.id
	us_nam = message.from_user.first_name
	username = message.from_user.username
	dr = dt_now 

	cursor = conn.execute("SELECT COUNT(*) from test WHERE user_id = ?", (message.from_user.id,))
	row = cursor.fetchone()
	if row[0] > 0:
		print(dt_now, 'login successfully by command: /report, id:', us_id, 'name:', us_nam)
		bot.send_message(message.chat.id, 'Отправьте адрес 👁')
		
		
		@bot.message_handler(content_types=['text'])
		def fun(message):
			dt_now = datetime.datetime.now()
			massage = message.text
			print(dt_now, 'Adres:',massage)
			print(dt_now, 'select photo')
			bot.send_message(message.chat.id, 'Отправьте фото 📸')
			# Сохраним изображение, которое отправил пользователь в папку `/files/%ID пользователя/photos`
			@bot.message_handler(content_types=['photo'])
			def save_photo(message):
				# создадим папку если её нет
				Path(f'files/{message.chat.id}/photos').mkdir(parents=True, exist_ok=True)

				# сохраним изображение
				file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
				downloaded_file = bot.download_file(file_info.file_path)
				src = f'files/{message.chat.id}/' + file_info.file_path
				print(dt_now, 'download to:', file_info.file_path)
				with open(src, 'wb') as new_file:
					new_file.write(downloaded_file)
					trl = 'files/' + str(us_id) + '/' + str(file_info.file_path)
					print(trl)
				bot.send_message(message.chat.id , 'Спасибо за доложение 🤝	')

				## явно указано имя файла!
				## откроем файл на чтение  преобразуем в base64
				#with open(f'files/{message.chat.id}/photos/file_0.jpg', "rb") as image_file:
				#	encoded_string = base64.b64encode(image_file.read())

				# откроем БД и запишем информацию (ID пользователя, base64, подпись к фото)
				conn = sqlite3.connect("database.db")
				cursor = conn.cursor()
				cursor.execute('INSERT INTO reports VALUES (?, ?, ?, ?)', (message.chat.id, massage,  trl, dt_now))
				conn.commit()


			# при получении команды /img от пользователя
			@bot.message_handler(commands=['img'])
			def ext_photo(message):
				# откроем БД и по ID пользователя извлечём данные base64
				conn = sqlite3.connect("test.db")
				img = conn.execute('SELECT img FROM users WHERE tlgrm_id = ?', (message.chat.id, )).fetchone()
				if img is None:
					conn.close()
					return None
				else:
					conn.close()
        
					# сохраним base64 в картинку и отправим пользователю
					with open("files/imageToSave.jpg", "wb") as fh:
						fh.write(base64.decodebytes(img[0]))
						bot.send_photo(message.chat.id, open("files/imageToSave.jpg", "rb"))



	else:
		dt_now = datetime.datetime.now()
		print(dt_now, "not found, reg:", us_id, ",", username, ",", us_nam)
		ded.db_table_val(user_id=us_id, user_name=us_nam, username=username, datareg = dr)
		bot.send_message(message.chat.id, 'Ваше имя добавлено в базу данных! \nПопробуйте сделать запрос снова!')
		
	us_id = message.from_user.id

bot.infinity_polling(none_stop=True)