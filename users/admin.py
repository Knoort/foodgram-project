from django.contrib import admin
from foodgram.autoregister import autoregister
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email', )


autoregister('users', )
