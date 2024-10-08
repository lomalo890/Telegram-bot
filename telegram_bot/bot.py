from telebot import TeleBot, types
import psycopg2 as ps
from frunzic import data

HOST = data(0)
DATABASE = data(1)
USER = data(2)
PASSWORD = data(3)

connection = ps.connect(
     host=HOST,
     user=USER,
     password=PASSWORD,
     database=DATABASE
)

cursor = connection.cursor()

people_table = '''
CREATE TABLE IF NOT EXISTS people (
     name TEXT NOT NULL,
     surname TEXT NOT NULL,
     age INTEGER
);
'''

cursor.execute(people_table)

connection.commit()
















bot = TeleBot(data(4));

name = '';
surname = '';
age = 0;

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');

def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age;
    try:
        age = int(message.text) #проверяем, что возраст введен корректно
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
        bot.register_next_step_handler(message, get_age)
        return
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_yes); 
    keyboard.add(key_no);
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )')
        cursor.execute(f'INSERT INTO people (name, surname, age) VALUES (\'{name}\', \'{surname}\', {age});')
        connection.commit()
    elif call.data == "no":
         bot.send_message(call.message.chat.id, 'Тогда ещё разок : (')
         start('message')


bot.polling(none_stop=True, interval=0)
cursor.close()
connection.close()