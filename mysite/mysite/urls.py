from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls.static import static

from mysite import settings

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/polls/', permanent=True)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)