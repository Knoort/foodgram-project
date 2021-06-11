"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls import handler404, handler500 #noqa
from django.conf.urls.static import static

handler404 = "recipes.views.page_not_found"   #noqa
handler500 = "recipes.views.server_error"     #noqa

urlpatterns = [
    #  регистрация и авторизация
    path("auth/", include("users.urls", namespace='users')),
    path('about/', include('about.urls', namespace='about')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'), name='api'),
    path('recipes/', include('recipes.urls', namespace='recipes')),


    # path('users/', include('users.urls'), name='users'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)