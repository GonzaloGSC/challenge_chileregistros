from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('bikesantiago/', include([
        path('load_data_bikesantiago', views.v_load_data_bikesantiago.as_view()),
    ])),
]

urlpatterns += staticfiles_urlpatterns()