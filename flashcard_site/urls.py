
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
<<<<<<< Updated upstream
=======
from django.contrib import admin
admin.autodiscover()

>>>>>>> Stashed changes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('flashcard_app.urls')),
    path('', RedirectView.as_view(url='')),
<<<<<<< Updated upstream
    path('accounts/', include('django.contrib.auth.urls'))
=======
    path('accounts/', include('django.contrib.auth.urls')),
    path('apis/v1/', include('apis.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
>>>>>>> Stashed changes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
