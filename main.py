import logging
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '6875090945:AAGYnOVPVEcdniQcIA0sAM-p5Z-BvI8ANqw'
ADMIN = 5707638365

# Инициализация бота и диспетчера с использованием MemoryStorage
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Инициализация базы данных SQLite
# Инициализация базы данных SQLite
try:
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        class TEXT
    )
    ''')
    conn.commit()
except Exception as e:
    logging.error(f"Failed to initialize the database: {e}")





conn.commit()
# Обработка команды /reg
@dp.message_handler(commands=['reg'])
async def cmd_start(message: types.Message, state: FSMContext):
    await message.reply("Привет! Давай зарегистрируем тебя.\nУкажи своё имя")
    await state.set_state(RegisterStates.first_name)

# Обработка состояний для регистрации
class RegisterStates:
    first_name = 'first_name'
    last_name = 'last_name'
    class_name = 'class_name'

# Обработка ответов на вопросы регистрации
@dp.message_handler(state=RegisterStates.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    async with state.proxy() as data:
        data[RegisterStates.first_name] = message.text
    await message.reply("Отлично! Теперь укажи свою фамилию.")
    await state.set_state(RegisterStates.last_name)

@dp.message_handler(state=RegisterStates.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    async with state.proxy() as data:
        data[RegisterStates.last_name] = message.text
    await message.reply("Хорошо! Какой у тебя класс?\nПример: 8Б")
    await state.set_state(RegisterStates.class_name)

@dp.message_handler(state=RegisterStates.class_name)
async def process_class_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[RegisterStates.class_name] = message.text
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Проверяем, существует ли запись с таким user_id
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Обновляем существующую запись
        cursor.execute("UPDATE users SET first_name=?, last_name=?, class=? WHERE user_id=?",
                       (data[RegisterStates.first_name], data[RegisterStates.last_name],
                        data[RegisterStates.class_name], user_id))
    else:
        # Вставляем новую запись
        user_data = (user_id, data[RegisterStates.first_name], data[RegisterStates.last_name],
                     data[RegisterStates.class_name])
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", user_data)

    conn.commit()

    await message.reply("Отлично! Ты зарегистрирован(а).\nЕсли отвои данные неверны, нажми команду /set")

    profile_text = f"Ты зарегистрирован(а)!\nИмя: {data[RegisterStates.first_name]}\nФамилия: {data[RegisterStates.last_name]}\nКласс: {data[RegisterStates.class_name]}"
    await message.reply(profile_text)


    # Закрываем соединение с базой данных
    conn.close()

    # Сбрасываем состояние
    await state.finish()


#########################################################
                      #set
@dp.message_handler(commands=['set'])
async def cmd_start(message: types.Message, state: FSMContext):
    await message.reply("Укажи своё новое имя")
    await state.set_state(RegisterStates.first_name)



# Обработка ответов на вопросы регистрации
@dp.message_handler(state=RegisterStates.first_name)

async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[RegisterStates.first_name] = message.text
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    await message.reply("Отлично! Теперь укажи свою новую фамилию.")
    await state.set_state(RegisterStates.last_name)

@dp.message_handler(state=RegisterStates.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[RegisterStates.last_name] = message.text
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    await message.reply("Хорошо! Какой у тебя новый класс?\nПример: 8Б")
    await state.set_state(RegisterStates.class_name)

@dp.message_handler(state=RegisterStates.class_name)
async def process_class_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[RegisterStates.class_name] = message.text
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Проверяем, существует ли запись с таким user_id
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Обновляем существующую запись
        cursor.execute("UPDATE users SET first_name=?, last_name=?, class=? WHERE user_id=?",
                       (data[RegisterStates.first_name], data[RegisterStates.last_name],
                        data[RegisterStates.class_name], user_id))
    else:
        # Вставляем новую запись
        user_data = (user_id, data[RegisterStates.first_name], data[RegisterStates.last_name],
                     data[RegisterStates.class_name])
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", user_data)

    conn.commit()

    await message.reply("Отлично! Ты изменил все свои данные.\nЕсли отвои данные снова неверны, нажми команду /set")

    profile_text = f"Ты зарегистрирован(а)!\n Новое имя: {data[RegisterStates.first_name]}\nНовая фамилия: {data[RegisterStates.last_name]}\nНовый класс: {data[RegisterStates.class_name]}"
    await message.reply(profile_text)


    # Закрываем соединение с базой данных
    conn.close()

    # Сбрасываем состояние
    await state.finish()













# Обработка команды /profil
@dp.message_handler(commands=['profil'])
async def cmd_profile(message: types.Message):
    # Открываем базу данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    # Закрываем соединение с базой данных
    conn.close()

    if user_data:
        profile_text = f"Имя: {user_data[1]}\nФамилия: {user_data[2]}\nКласс: {user_data[3]}"
        await message.reply(profile_text, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await message.reply("Ты еще не зарегистрирован(а). Используй /reg.")

# Оставшийся код шахматного турнира
tournament_date = datetime(2023, 11, 30, 12, 00)

class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    conn = sqlite3.connect('users.db')




    cur = conn.cursor()
    cur.execute(f"SELECT user_id FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    await message.answer('Привет, мы тебя приглашаем на шахматный турнир.\n'
                         '*********************************************\n'
                         '                           Нажми            \n'
                          "/reg - Зарегистрироваться на шахматном турнире\n"
                          "/set - Обновить свои данные после регистрации\n"
                          "/profil - Посмотреть свой профиль\n"
                          "/buy - Получить билеты на шахматный турнир\n"
                          "/time - Узнать, сколько времени осталось до турнира\n"
                          "/info - Получить информацию о шахматном турнире\n"
                          "/help - посмотреть подробности турнира")
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Пользователи"))
        await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=keyboard)
    else:
        if result is None:
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
            entry = cur.fetchone()
            if entry is None:
                cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
            conn.commit()
            await message.answer('Привет')
        else:
            print("Вошёл пользователь без админки")


@dp.message_handler(commands=['buy'])
async def start(message: types.Message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    # Закрываем соединение с базой данных
    conn.close()

    if user_data:
        # profile_text = f"Имя: {user_data[1]}\nФамилия: {user_data[2]}\nКласс: {user_data[3]}"
        # await message.reply(profile_text, parse_mode=types.ParseMode.MARKDOWN)
        await message.answer(f"Чтобы получить билеты {user_data[1]} {user_data[2]} напиши в личку @RuziboevMuhammadsulton\n")
    else:
        await message.reply("Ты еще не зарегистрирован(а). Используй /reg.")





@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.answer("дата: {} \n""число: {} \n""место: {} \n".format(tournament_date.strftime("%d.%m.%Y"), tournament_date.strftime("%d"),"Школа 160\n"
                                             "*********************************************\n"
                                             "если хочешь узнать подробные сведения о дате, команда /time\n"
                                             "/reg чтобы участвовать в турнире, надо зарегистрироваться"))


@dp.message_handler(commands=['admin_info'])
async def cmd_start(message: types.Message):
    await message.answer("Создатель бота:@Pumpkin2008\n"
                        "Созадатель шахматного турнира @RuziboevMuhammadsulton")



@dp.message_handler(commands=['time'])
async def send_time(message):
    now = datetime.now()
    difference = tournament_date - now
    days = difference.days
    hours = difference.seconds // 3600
    minutes = (difference.seconds // 60) % 60
    await bot.send_message(message.chat.id, "До турнира осталось {} дней, {} часов и {} минут".format(days, hours, minutes), reply_to_message_id=message.message_id)

@dp.message_handler(commands=['info'])
async def start(message: types.Message):
    await message.answer("Это самый большой турнир в Школе 160\n""*********************************************\n"
                         "Мы приглашаем тебя на бесплатный урнир\n"
                         "*********************************************\n"
                         "Призовой фонд \n"
                         "1 место - Грамота за 1-е место\n"
                         "2 место - Грамота за 2-е место\n"
                         "3 место - Грамота за 3-е место\n"
                         "*********************************************\n"
                         #"билеты на закрытую вечеринку в Школе №160\n"
                         "/reg чтобы участвовать в турнире, надо зарегистрироваться ")

@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: types.Message):
    if message.from_user.id == ADMIN:
        await dialog.spam.set()
        await message.answer('Напиши текст рассылки')
    else:
        await message.answer('Вы не являетесь админом')

@dp.message_handler(state=dialog.spam)
async def start_spam(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Пользователи"))
        await message.answer('Главное меню', reply_markup=keyboard)
        await state.finish()
    else:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute(f'''SELECT user_id FROM users''')
        spam_base = cur.fetchall()
        print(spam_base)
        for z in range(len(spam_base)):
            print(spam_base[z][0])
        for z in range(len(spam_base)):
            await bot.send_message(spam_base[z][0], message.text)
        await message.answer('Рассылка завершена')

        # conn.close()
        #
        # # Сбрасываем состояние
        # await state.finish()

        await state.finish()

@dp.message_handler(state='*', text='Назад')
async def back(message: types.Message):
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Пользователи"))
        await message.answer('Главное меню', reply_markup=keyboard)
    else:
        await message.answer('Вам не доступна эта функция')









#для админки пользователи
@dp.message_handler(content_types=['text'], text='Пользователи')
async def cmd_users(message: types.Message):
    if message.from_user.id == ADMIN:
        # Открываем базу данных
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        all_users = cursor.fetchall()

        # Закрываем соединение с базой данных
        conn.close()

        users_text = "Список зарегистрированных пользователей:\n"
        for user in all_users:
            if len(user) >= 4:
                users_text += f"(Имя: {user[1]} | Фамилия: {user[2]} | Класс: {user[3]})\n"
                # (ID: {user[0]} выдает iD users
            else:
                users_text += f"Ошибка: Неправильный формат данных пользователя\n"

        await message.reply(users_text, parse_mode=types.ParseMode.MARKDOWN)

    else:
        await message.answer('Вы не являетесь админом')








if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
