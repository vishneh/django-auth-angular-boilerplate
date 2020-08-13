from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include
import account

urlpatterns = [
    path('o/', include('account.urls')),
    path('admin/', admin.site.urls),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
# For the Image View outside API