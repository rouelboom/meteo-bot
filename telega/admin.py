from django.contrib import admin

from .models import TelegramUser, Things


class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'creation_date', 'last_login_date')
    search_fields = ('username',)


admin.site.register(TelegramUser, TelegramUsersAdmin)
