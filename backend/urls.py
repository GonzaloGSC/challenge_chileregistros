from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bikesantiago/', include('apps.bikesantiago.api.urls')),
    path('seia/', include('apps.seia.api.urls')),
    path('auth/', include('rest_framework.urls'))
]

urlpatterns += staticfiles_urlpatterns()