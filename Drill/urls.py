from django.urls import path
#from . import views
from .views import upload
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [   

    path('upload/', upload, name='upload'),
   
]
# Append the static media configuration
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)