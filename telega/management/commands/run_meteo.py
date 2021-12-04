import os
import asyncio
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

import requests
import transliterate

import logging
from dotenv import load_dotenv

load_dotenv()

from telega.models import Things, TelegramUser, MeteoData, CityData
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
WEATHER_APP_ID = os.getenv('OPEN_WEATHER_API_KEY')


def create_new_city(city):
    city_transliterated = transliterate.translit(city.lower(), language_code='ru', reversed=True)
    print(city_transliterated)

    city_and_country = f'{city_transliterated},RU'
    looking_id = None
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city_and_country, 'type': 'like',
                                   'lang': 'ru',
                                   'units': 'metric', 'APPID': WEATHER_APP_ID})
        data = res.json()
        print(data)
        for item in data['list']:
            if item['name'].lower() == city_transliterated:
                print(item['name'].lower(), city_transliterated)
                info = item
                looking_id = item['id']
                break

    except Exception:
        pass



def get_current_meteo_data(city) -> dict:
    # city_query = CityData.objects.filter(city_ru=city.lower())
    # if city_query.count() == 0:
    #     pass

    if city.lower() == 'москва':
        city_transliterated = 'moscow'
    elif city.lower() in ['питер', 'санкт-петербург']:
        city_transliterated = 'saint petersburg'
    else:
        city_transliterated = transliterate.translit(city.lower(), language_code='ru', reversed=True)
    print(city_transliterated)

    city_and_country = f'{city_transliterated},RU'
    looking_id = None
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city_and_country, 'type': 'like',
                                   'lang': 'ru',
                                   'units': 'metric', 'APPID': WEATHER_APP_ID})
        data = res.json()
        print(data)
        for item in data['list']:
            if item['name'].lower() == city_transliterated:
                print(item['name'].lower(), city_transliterated)
                info = item
                looking_id = item['id']
                break
        if looking_id is None:
            return {'error': 'город не найден'}

        # res = requests.get("http://api.openweathermap.org/data/2.5/weather",
        #                    params={'id': looking_id, 'units': 'metric', 'lang': 'ru',
        #                            'APPID': weather_api_id})
        # info = res.json()
        # print(info)
        weather = {
            'description': info['weather'][0]['description'],
            'temp': info['main']['temp'],
            'feels_like': info['main']['feels_like'],
            'humidity': info['main']['humidity'],
            'city': transliterate.translit(info['name'], language_code='ru'),
            'wind_speed': info['wind']['speed']
        }

        # print(weather)

        # mgr.one_call()
        return weather
    except Exception as e:
        print("Exception (weather):", e)
        pass


async def run_meteo():
    get_current_meteo_data('Санкт-Петербург')


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            asyncio.run(run_meteo())
        except KeyError:
            raise CommandError('Poll "%s" does not exist' % 1)

        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % 1))