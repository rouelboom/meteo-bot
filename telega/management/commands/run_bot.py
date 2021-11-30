import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

import logging
import telebot

from telega.models import Things, TelegramUser
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot('2102394221:AAGYEsIv5gCUJabqWDMZYJjNlUDxh54W78U')


@bot.message_handler(commands=['qwe', 'login'])
def login_into_bot(message):
    try:
        username = message.from_user.username
        id = message.from_user.id
        print(username)
        current_user = TelegramUser.objects.all().filter(user_telegra_id=id)
        # now_time = datetime.datetime.now()
        now_time = timezone.now()
        if current_user.count() == 0:
            print('A')
            TelegramUser.objects.create(
                user_telegra_id=id,
                username=username,
                first_name=message.from_user.first_name,
                creation_date=now_time,
                last_login_date=now_time)
        else:
            print('B')
            current_user.update(last_login_date=now_time)
    except KeyError as e:
        pass


@bot.message_handler(commands=['start', 'help', 'login'])
# @bot.message_handler(func=lambda message: 's' in str(message))
def send_welcome(message):
    try:
        print(message.message_id)
        # bot.reply_to(message, "Howdy, how are you doing?")
        bot.send_message(message.chat.id, 'man that is nice')
        bot.send_message(message.chat.id, message)
    except AttributeError:
        pass


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