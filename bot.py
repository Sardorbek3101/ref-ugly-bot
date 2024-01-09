import telebot
import psycopg2

from config import host, user, password, db_name
from telebot import types

try:
    connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host
        )
    cursor = connection.cursor()

except Exception as ex:
    print("connection refursed ...")
    print(ex)

BOT_TOKEN = ("6061714192:AAE4UHTllJpt4TZv4bDOpuxXrhczLDrRHZw")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


def check_member(chat_id, call_id=""):
    chanels = cursor.execute("Select * from chanels")
    chanels = cursor.fetchall()
    if chanels:
        false_chanels = []
        try:
            for chanel in chanels:
                chat_member = bot.get_chat_member(chanel[1], chat_id)
                if chat_member.status == "member" or chat_member.status == "creator" or chat_member.status == "administrator":
                    pass
                else:
                    false_chanels.append(chanel)
        except:
            pass
            
        if false_chanels:
            try:
                bot.answer_callback_query(callback_query_id=call_id, text='Вы не подписаны на все каналы')
            except:
                pass
            link_buttons = types.InlineKeyboardMarkup()
            for chan in false_chanels:
                link_buttons.row(types.InlineKeyboardButton(text="Подписаться", url=chan[2]))
            check_butt = types.InlineKeyboardButton(text="Проверить ✅", callback_data="menu")
            link_buttons.row(check_butt)
            bot.send_message(chat_id, "Для начала подпишитесь на наши каналы 🔽", reply_markup=link_buttons)
        else:
            bot.send_message(chat_id, "Меню нахуй")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать!")
    check_member(message.chat.id)



@bot.callback_query_handler(func = lambda call: True)
def ansver(call):
    check_member(call.message.chat.id, call.id)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


bot.infinity_polling()