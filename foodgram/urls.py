from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls import handler404, handler500  #noqa
from django.conf.urls.static import static

handler404 = 'recipes.views.page_not_found'   #noqa
handler500 = 'recipes.views.server_error'     #noqa

urlpatterns = [
    #  регистрация и авторизация
    path('auth/', include('users.urls', namespace='users')),
    path('about/', include('about.urls', namespace='about')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'), name='api'),
    path('recipes/', include('recipes.urls', namespace='recipes')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
