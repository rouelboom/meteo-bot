import os
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

import logging
import telebot
from telebot import types

from .run_meteo import get_current_meteo_data
from telega.const import BAD_WORDS, WEATHER_WORDS
from telega.models import TelegramUser
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


def check_login(message):
    user_id = message.from_user.id
    user = TelegramUser.objects.filter(user_telega_id=user_id)
    if user.count() != 0:
        login_into_bot(message)


def login_into_bot(message):
    try:
        username = message.from_user.username
        id = message.from_user.id
        print(username)
        current_user = TelegramUser.objects.filter(user_telega_id=id)
        # now_time = datetime.datetime.now()
        now_time = timezone.now()
        if current_user.count() == 0:
            print(message.from_user)
            return TelegramUser.objects.create(
                user_telega_id=id,
                username=username,
                first_name=message.from_user.first_name,
                creation_date=now_time,
                last_login_date=now_time
            )

        else:
            current_user.update(last_login_date=now_time)
            return current_user
    except KeyError as e:
        pass


@bot.message_handler(commands=['start'])
# @bot.message_handler(func=lambda message: 's' in str(message))
def send_welcome(message):
    try:
        # bot.reply_to(message, "Howdy, how are you doing?")
        login_into_bot(message)
        bot.send_message(message.chat.id, (f'Просто здравствуй, {message.from_user.first_name}.\n'
                                           'Просто как дела?'))

    except AttributeError:
        pass


@bot.message_handler(commands=['clear_chat'])
def clear_chat(message):
    try:
        print('we are in clear chat')
        last_message = message.message_id
        chat_id = message.chat.id
        a = types.ChatPermissions(can_invite_users=True)
        print(last_message)
        flag = bot.get_chat_administrators(chat_id)
        for message in range(10, last_message):
            print(message)
            bot.delete_message(chat_id, message)

    except AttributeError:
        pass


@bot.message_handler(commands=['secret'])
def secret_message(message):
    try:
        print(message.message_id)
        bot.send_message(message.chat.id, 'Настюша Наумова, я тебя люблю :) <3')
    except AttributeError:
        pass


@bot.message_handler(commands=['unban'])
def unban_handler(message):
    user = login_into_bot(message)
    user.update(ban=False)
    bot.send_message(message.chat.id, 'Вы были разблокированы')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def default_command(message):
    # first need to check user to ban\block
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = TelegramUser.objects.filter(user_telega_id=user_id)
    if user.count() != 0:
        user = login_into_bot(message)
    if user[0].ban:
        bot.send_message(chat_id, 'Вам запрещенно общаться с этим ботом')
        return
    # print(user.ban)
    for word in BAD_WORDS:
        if word in message.text:
            user.update(ban=True, ban_date=timezone.now())
            bot.send_message(chat_id, "У нас не ругаются. Вы в бане")
            return

    for weather_word in WEATHER_WORDS:
        if weather_word in message.text:
            text = message.text
            text_list = text.split(' ')
            if len(text_list) == 2:
                for word in text_list:
                    if word not in WEATHER_WORDS:
                        result = get_current_meteo_data(word)
                        if result.get('error'):
                            bot.send_message(chat_id, f"Что-то пошло не так: {result['error']}'")
                            break
                        else:
                            info_message = f'Погода в городе {result["city"]}:\n' \
                                           f'Температура {result["temp"]}, {result["description"]}\n' \
                                           f'Ощущается как {result["feels_like"]}\n' \
                                           f'Скорость ветра {result["wind_speed"]}м/с\n'
                            bot.send_message(chat_id, info_message)
                            break

                break
        else:
            bot.send_message(chat_id, ("Кажется хотите узнать погоду?"
                                       "Укажите город, допустим: 'погода Калуга'"))
            break


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('qwe', nargs='*', type=int, )  # позиционный аргумент
        parser.add_argument('-a', '--admin', action='store_true',
                            help='Создание учетной записи администратора', required=False)  # флаговый аргумент
        parser.add_argument('-p', '--prefix', type=str, help='Префикс для username', required=False)  # именованный аргумент

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete poll instead of closing it',
        )
        # Optional argument

    def handle(self, *args, **options):
        try:
            total = options.get('qwe')
            prefix = options.get('prefix')
            admin = options.get('admin')

            print(total)
            print(prefix)
            print(admin)

            bot.infinity_polling()
            # Things.objects.create(some=len(total))
            # if options.get('qwe'):
            #     print('qweqwe')
            # print('hello world')
            # if options.get('prefix'):
            #     print(options['prefix'])
            # self.stdout.write('hello world11')
            # poll = Poll.objects.get(pk=poll_id)
            # print(Things.objects.all())
        except KeyError:
            raise CommandError('Poll "%s" does not exist' % 1)

        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % 1))