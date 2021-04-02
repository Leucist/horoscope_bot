import random
import telebot

from telebot import types

TOKEN = "1734793624:AAGZH62rmABiP1O1_LT3ZzbT0MnVNK7SF1E"

bot = telebot.TeleBot(TOKEN)

signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]

s = ["Этот день кажется непростым, но не спешите отчаиваться: ",
     "Мало таких однозначных дней, как этот, ",
     "Вторая половина дня обещает денежные поступления, ",
     "Это подходящее время для решения любых вопросов, ",
     "Легко сохранять спокойствие в первой половине дня, ",
     "Вторая половина дня проходит плодотворно и приятно, ",
     "Вы более эмоциональны, чем обычно, но ",
     "День начинается удачно. Этим стоит воспользоваться, ",
     "Вторая половина дня проходит очень спокойно, ",
     "Гармонично складываются события всего дня, ",
     "Кое-какие трудности могут возникнуть, но день сложится удачно, ",
     "Ситуация часто меняется, порой приходится принимать решения на ходу, "]
m = ["важно не сердиться из-за пустяков, ",
     "нужно постараться сохранять дружелюбие и жизнерадостность, ",
     "Вы легко сможете преодолеть все трудности",
     "звезды говорят(со мной, я это знаю!), Вы не поддадитесь на провокации, ",
     "Вы всегда можете держать себя в руках — сегодня Вам это особенно сыграет на руку, ",
     "Вашему знаку зодиака будет несколько проще. Не зря говорят, что удача сопутствует ему, ",
     "возможны новые открытия, приятные известия, предложения, от которых не захочется отказываться, ",
     "удача на вашей стороне, ",
     "Вы находите общий язык с разными людьми, отлично ладите даже с теми, кого прежде не понимали, ",
     "многие разногласия останутся в прошлом, ",
     "Вам почти не придется прикладывать усилий для того, чтобы что-то хорошее произошло, ",
     "Вы радуетесь интересным задачам, с энтузиазмом беретесь за дела, которые другим показались слишком сложными, "]
l = ["сейчас нужно сгладить острые углы во взаимоотношениях с близкими.",
     "старайтесь избегать конфликтов.",
     "главное — не сдавайтесь и верьте в себя!",
     "ситуация вскоре изменится к лучшему, общаться со знакомыми станет гораздо проще.",
     "могут появиться хорошие идеи, связанные с развитием вашей карьеры или бизнеса.",
     "жизнь будет открывать новые возможности и радовать удачными совпадениями!",
     "старайтесь не тратить время напрасно и действовать решительно.",
     "Вы добьетесь даже большего, чем ожидали.",
     "Вы обретете достаточно жизненного опыта и постараетесь не повторить своих прошлых ошибок.",
     "постарайтесь осуществить то, что было задумано давным-давно.",
     "прислушайтесь к интуиции: благодаря ее подсказкам вы не допустите ошибок, осуществите все, что задумали.",
     "не исключены удачные совпадения, которые откроют перед вами новые возможности!"]


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/horoscope"))
    bot.send_message(message.chat.id,
                     "Здравствуйте, {0.first_name}. Хоба — гороскоп. Вот он самый. Тут.".format(message.from_user),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['horoscope'])
def horoscope(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for si in signs:
        markup.add(types.KeyboardButton(si))
    sent = bot.send_message(message.chat.id, "Выберите Ваш знак зодиака:", reply_markup=markup)
    bot.register_next_step_handler(sent, second_func)


@bot.message_handler(content_types=['text'])
def chat(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/horoscope"))
    bot.send_message(message.chat.id, "Я ничего не понимаю. Пожалуйста, выберите команду", reply_markup=markup)


def second_func(message):
    sign = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Завтра")
    item2 = types.KeyboardButton("Сегодня")
    item3 = types.KeyboardButton(str(random.randint(10, 28)) + "." + str(random.randint(1, 12)))
    markup.add(item1, item2, item3)
    sent = bot.send_message(message.chat.id, "На какой день Вы хотите получить гороскоп?", reply_markup=markup)
    bot.register_next_step_handler(sent, third_func, sign)


def third_func(message, sign):
    day = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/horoscope"))
    i1 = random.randint(0, 11)
    i2 = random.randint(0, 11)
    i3 = random.randint(0, 11)
    bot.send_message(message.chat.id,
                     "Ваш гороскоп на " + day.lower() + ".\n" + sign.title() + ".\n" + s[i1] + m[i2] + l[i3],
                     reply_markup=markup)


bot.polling(none_stop=True)
