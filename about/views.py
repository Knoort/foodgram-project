from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    page = None
    template_name = 'about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page == 'author':
            context['about_title'] = 'Об авторе'
            context['about_text'] = 'Здесь будет раздел "Обо мне"'
        elif self.page == 'tech':
            context['about_title'] = 'Технологии'
            context['about_text'] = 'Здесь будет описание программных средств'

        return context