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


def create_new_city(city) -> int:
    city_transliterated = transliterate.translit(city.lower(), language_code='ru', reversed=True)
    print(city_transliterated)

    city_and_country = f'{city_transliterated},RU'
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city_and_country, 'type': 'like',
                                   'lang': 'ru',
                                   'units': 'metric', 'APPID': WEATHER_APP_ID})
        data = res.json()
        print(data)
        if data.get('list') is None:
            print('data list is none')
            return -1
        if len(data['list']) == 1:
            item = data['list'][0]
            new_city = CityData.objects.create(
                city_id=item['id'],
                name=item['name'],
                name_ru=city.lower(),
                latitude=item['coord']['lat'],
                longitude=item['coord']['lon'],
                county_prefix=item['sys']['country'],
            )
            return new_city.city_id
        city_id = -1
        # if len(data['list'] == 2):
        #     if data['list'][0]['coord']['lat'] -
        for item in data['list']:
            new_city = CityData.objects.create(
                city_id=item['id'],
                name=item['name'],
                name_ru=city.lower(),
                latitude=item['coord']['lat'],
                longitude=item['coord']['lon'],
                county_prefix=item['sys']['country'],
            )
            if len(item['name'].split(' ')) == len(list(city)):
                print('we are here')
                city_id = new_city.id
        return city_id

    except Exception:
        pass


def get_current_meteo_data(city) -> dict:
    city_query = CityData.objects.filter(name_ru=city.lower())
    if city_query.count() == 0:
        city_id = create_new_city(city)
        if city_id == -1:
            return {'error': 'город не найден'}
    else:
        city_id = city_query[0].city_id

        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru',
                                   'APPID': WEATHER_APP_ID})
        info = res.json()
        print(info)
        weather = {
            'description': info['weather'][0]['description'],
            'temp': info['main']['temp'],
            'feels_like': info['main']['feels_like'],
            'humidity': info['main']['humidity'],
            'city': transliterate.translit(info['name'], language_code='ru'),
            'wind_speed': info['wind']['speed']
        }

        print(weather)

        # mgr.one_call()
        return weather


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