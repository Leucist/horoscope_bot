import random
import telebot

from telebot import types

TOKEN = "1734793624:AAGZH62rmABiP1O1_LT3ZzbT0MnVNK7SF1E"

bot = telebot.TeleBot(TOKEN)

adm_functions = ['Рассылка', 'Отправить сообщение-вопрос', 'Просмотреть БД']
admin_id = 1064282294

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
     "Вы легко сможете преодолеть все трудности ",
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


@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == admin_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for function in adm_functions:
            item = types.KeyboardButton(function)
            markup.add(item)
        item = types.KeyboardButton("Назад ➤")
        markup.add(item)
        sent = bot.send_message(admin_id, "Что бы Вы хотели сделать?", reply_markup=markup)
        bot.register_next_step_handler(sent, admin_after)
    else:
        bot.send_message(message.chat.id, "У Вас недостаточно прав для использования этой функции.")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/horoscope"))
    bot.send_message(message.chat.id,
                     "Здравствуйте, {0.first_name}. Хоба — гороскоп. Вот он самый. Тут.".format(message.from_user),
                     parse_mode='html', reply_markup=markup)


def admin_after(message):
    markup = back_markup()
    if message.from_user.id == admin_id:
        if message.text == "Рассылка":
            sent = bot.send_message(message.chat.id, "Какое сообщение Вы хотите разослать?")
            bot.register_next_step_handler(sent, mailing)
        elif message.text == "Просмотреть БД":
            show_database()
        elif message.text == "Отправить сообщение-вопрос":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Всем")
            item2 = types.KeyboardButton("Выбрать пользователя")
            markup.add(item1, item2)
            sent = bot.send_message(message.chat.id,
                                    "Разослать опрос всем пользователям или выбрать конкретного пользователя?",
                                    reply_markup=markup)
            bot.register_next_step_handler(sent, admin_after)
        elif message.text.lower() == 'всем':
            sent = bot.send_message(message.chat.id, "Опрос на какую тему Вы хотите провести?", reply_markup=None)
            bot.register_next_step_handler(sent, mailing, arguments=True)
        elif message.text == 'Выбрать пользователя':
            sent = bot.send_message(message.chat.id, "Выберите желаемого пользователя и отправьте его id",
                                    reply_markup=None)
            bot.register_next_step_handler(sent, q_user)
        elif message.text == "Назад ➤":
            bot.send_message(message.chat.id, "Принято.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "У Вас недостаточно прав для использования этой функции.",
                         reply_markup=markup)


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


def initialisation(message):
    pid = message.from_user
    all_data = {}
    filename = "user_base.json"
    with open(filename, "r", encoding="UTF-8") as database:
        data = json.loads(database.read())
        for i in data['users']:
            if i['id'] == pid.id:
                break
        else:
            amount = int(data['items']) + 1
            data = data['users']
            user = {"id": pid.id, "first_name": pid.first_name, "last_name": pid.last_name,
                    "username": pid.username, "is_bot": pid.is_bot}
            data.append(user)
            all_data['items'] = amount
            all_data['users'] = data
            write_database(all_data, filename)


def q_user(message):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        markup = back_markup()
        bot.send_message(admin_id,
                         "Ошибка: Неверный формат id.\nПроверьте правильность введенных данных и попробуйте снова.",
                         reply_markup=markup)
        return 1
    else:
        sent = bot.send_message(admin_id, "Какой вопрос Вы хотели бы задать?\n(Отправьте его следующим сообщением)")
        bot.register_next_step_handler(sent, mailing, arguments=True, user_id=user_id)


def mailing(message, arguments=None, user_id=None):
    markup = back_markup()
    with open("userbase.json", "r", encoding="UTF-8") as database:
        data = json.loads(database.read())
        if arguments:
            if user_id is not None:
                try:
                    sent = bot.send_message(user_id, message.text, reply_markup=markup)
                    bot.register_next_step_handler(sent, feedback, message.text)
                except ApiException:
                    bot.send_message(admin_id,
                                     "Вопрос не был отправлен, т.к. пользователь заблокировал бота или отправка сообщений ему невозможна.",
                                     reply_markup=markup)
                    return 0
                else:
                    return 0
            for u_id in data:
                try:
                    if int(u_id) != message.from_user.id:
                        sent = bot.send_message(u_id, message.text, reply_markup=markup)
                        bot.register_next_step_handler(sent, feedback, message.text)
                    else:
                        bot.send_message(message.chat.id, "Принято.", reply_markup=markup)
                except ApiException:
                    continue
                else:
                    continue
            return 0
        if message.content_type == 'text':
            for u_id in data:
                try:
                    if int(u_id) != message.from_user.id:
                        bot.send_message(u_id, message.text, reply_markup=markup)
                    else:
                        bot.send_message(message.chat.id, "Принято.", reply_markup=markup)
                except ApiException:
                    continue
                else:
                    continue
            bot.send_message(message.chat.id, "Разослано.", reply_markup=markup)
        elif message.content_type == 'photo':
            raw = message.photo[2].file_id
            name = "mailing.jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(name, "wb") as photo:
                photo.write(downloaded_file)
            for u_id in data:
                photo = open(name, "rb")
                try:
                    if int(u_id) != message.from_user.id:
                        bot.send_photo(u_id, photo, reply_markup=markup)
                    else:
                        bot.send_message(message.chat.id, "Принято.", reply_markup=markup)
                except ApiException:
                    photo.close()
                    continue
                else:
                    photo.close()
                    continue
            bot.send_message(message.chat.id, "Разослано.", reply_markup=markup)
        elif message.content_type == 'document':
            raw = message.document.file_id
            name = "mailing" + message.document.file_name[-4:]
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(name, "wb") as document:
                document.write(downloaded_file)
            for u_id in data:
                document = open(name, "rb")
                try:
                    if int(u_id) != message.from_user.id:
                        bot.send_document(u_id, document, reply_markup=markup)
                    else:
                        bot.send_message(message.chat.id, "Принято.", reply_markup=markup)
                except ApiException:
                    document.close()
                    continue
                else:
                    document.close()
                    continue
            bot.send_message(message.chat.id, "Разослано.", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Неподдерживаемый тип сообщения", reply_markup=markup)


def feedback(message, question):
    bot.send_message(admin_id,
                     'Ответ на Ваш вопрос "' + question + '" — "' + message.text + '" от:\n(id) ' + str(
                         message.from_user.id) + ',\n(name) '
                     + str(message.from_user.first_name))
    bot.send_message(message.chat.id, "Принято.\nБлагодарим за ответ!)")


def show_database():
    try:
        with open("userbase.json", "r", encoding="UTF-8") as database_file:
            bot.send_document(admin_id, database_file)
    except FileNotFoundError:
        bot.send_message(admin_id, '[Ошибка] Файл БД "userbase.json" не найден.')


def write_database(data, filename):
    with open(filename, "w", encoding="UTF-8") as database:
        json.dump(data, database, indent=1, ensure_ascii=False, separators=(',', ':'))


bot.polling(none_stop=True)
