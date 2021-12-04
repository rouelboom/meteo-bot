from django.contrib import admin

from .models import TelegramUser, CityData


class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'creation_date', 'last_login_date', 'ban', 'ban_date')
    search_fields = ('username',)


class CityDataAdmin(admin.ModelAdmin):
    list_display = ('city_id', 'name', 'name_ru', 'county_prefix', 'latitude', 'longitude')
    list_editable = ('name', 'name_ru', 'county_prefix')


admin.site.register(TelegramUser, TelegramUsersAdmin)
admin.site.register(CityData, CityDataAdmin)
