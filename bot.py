import telebot, datebase as db, buttons as bt
from geopy import Nominatim

# Создать объект бота
bot = telebot.TeleBot('6840296569:AAGuz7W67cXWpg6tyaN8PWNEhnq5ijz0LRg')
# Использование карт
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
# Временные данные
users = {}


# Обработка команды start
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    # Проверка пользователя
    check = db.checker(user_id)
    if check:
        bot.send_message(user_id, f'Привет, {message.from_user.first_name}!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Что ты хочешь?', reply_markup=bt.main_menu_buttons())
        bot.register_next_step_handler(message, chatting)
    else:
        bot.send_message(user_id, "Здравствуйте, добро пожаловать! Давайте начнем "
                                  "регистрацию, введите свое имя!")
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


@bot.message_handler(commands=['English'])
def start_message_eng(message):
    user_id = message.from_user.id
    bot.send_message(user_id, f'Hi, {message.from_user.first_name}!', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(user_id, 'What are you doing?', reply_markup=bt.main_menu_buttons_eng())
    bot.register_next_step_handler(message, chatting)


def chatting(message):
    user_id = message.from_user.id
    if message.text == 'Узнать тайну всего мира!':
        bot.send_message(user_id, 'Не расскажу тебе!', reply_markup=bt.ok())
        bot.register_next_step_handler(message, start_message)
    elif message.text == 'Помощь':
        bot.send_message(user_id, 'Как я тебе могу помочь?')
        bot.send_message(user_id, 'Хотя мне лень, не помогу...', reply_markup=bt.ok())
        bot.register_next_step_handler(message, start_message)
    elif message.text == 'Язык':
        bot.send_message(user_id, 'Выбери язык!', reply_markup=bt.languages())
        bot.register_next_step_handler(message, proverka)
    elif message.text == 'The secret of the whole world!':
        bot.send_message(user_id, 'I will not able to say it!', reply_markup=bt.ok())
        bot.register_next_step_handler(message, start_message_eng)
    elif message.text == 'Help':
        bot.send_message(user_id, 'How am I help you?')
        bot.send_message(user_id, 'I am not help you because i am tired!', reply_markup=bt.ok())
        bot.register_next_step_handler(message, start_message_eng)
    elif message.text == 'Languages':
        bot.send_message(user_id, 'Choose language!', reply_markup=bt.languages())
        bot.register_next_step_handler(message, proverka)
    else:
        bot.send_message(user_id, 'Опять ты что-то сломал 🤬')
        bot.register_next_step_handler(message, start_message)

        
def proverka(message):
    user_id = message.from_user.id
    if message.text == 'Русский':
        bot.send_message(user_id, 'Вы выбрали русский язык!', reply_markup=bt.ok())
        bot.register_next_step_handler(message, start_message)
    elif message.text == 'English':
        bot.send_message(user_id, 'You choose english!', reply_markup=bt.ok())
        bot.register_next_step_handler(message, start_message_eng)


# Этап получения имени
def get_name(message):
    name = message.text
    user_id = message.from_user.id
    bot.send_message(user_id, "Отлично, а теперь отправьте номер!",
                     reply_markup=bt.num_bt())
    # Этап получения номера
    bot.register_next_step_handler(message, get_number, name)


# Этап получения номера
def get_number(message, name):
    user_id = message.from_user.id
    # Если юзер отправил номер по кнопке
    if message.contact:
        number = message.contact.phone_number
        bot.send_message(user_id, 'Супер! Последний этап: отправь локацию',
                         reply_markup=bt.loc_bt())
        # Этап получения локации
        bot.register_next_step_handler(message, get_location, name, number)
    # Если юзер отправил номер не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку',
                         reply_markup=bt.num_bt())
        # Этап получения номера
        bot.register_next_step_handler(message, get_number, name)


# Этап получения локации
def get_location(message, name, number):
    user_id = message.from_user.id
    # Если юзер отправил локацию по кнопке
    if message.location:
        location = str(geolocator.reverse(f'{message.location.latitude}, '
                                          f'{message.location.longitude}'))
        db.register(user_id, name, number, location)
        bot.send_message(user_id, 'Регистрация прошла успешно',
                         reply_markup=bt.ok())
        bot.register_next_step_handler(message, start_message)
    # Если юзер отправил локацию не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку',
                         reply_markup=bt.loc_bt())
        # Этап получения номера
        bot.register_next_step_handler(message, get_location, name, number)


bot.polling(none_stop=True)
