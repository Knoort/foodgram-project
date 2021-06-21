from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Паттерн страницы пользователя совпадает с этими путями
RESTRICTED_USERNAMES = (
    'new',
    'favorites',
    'subscriptions',
    'purchases'
)

User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', )

    def clean_username(self):
        username = self.cleaned_data['username']
        if username in RESTRICTED_USERNAMES:
            raise ValidationError('Запрещенное имя пользователя!')
        return username
