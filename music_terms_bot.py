import telebot
import psycopg2
bot = telebot.TeleBot('token')
conn = psycopg2.connect('postgres://user:password@localhost:port/table_name')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Введи музыкальный термин, а я отправлю тебе его перевод и описание!')

@bot.message_handler()
def message(message):
    bot.send_message(message.chat.id, f'Общаться я не умею, поэтому, {message.from_user.first_name}, Введи музыкальный термин, а я отправлю тебе его перевод и описание!')
    bot.register_next_step_handler(message, send_description)
def send_description(message):
    try:
        # пытаемся подключиться к базе данных
        conn = psycopg2.connect('postgres://user:password@localhost:port/table_name')
    except:
        # в случае сбоя подключения будет выведено сообщение в STDOUT
        print('Can`t establish connection to database')

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music_terms where term = '%s'" % (message.text.strip()))
    terms = cursor.fetchall()
    info = ''
    for el in terms:
        info += f'{el[1]} значит: {el[2]}\n'
    cursor.close()
    conn.close()

    bot.send_message(message.chat.id, info )
bot.infinity_polling()

