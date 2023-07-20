from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'tg_chat_id', 'tg_user_id', 'verification_code', 'position', 'category')
    list_filter = ('position',)
    readonly_fields = list_display
