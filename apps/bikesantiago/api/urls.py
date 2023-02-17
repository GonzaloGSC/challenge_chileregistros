from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path("", include([
        path('networks/', views.v_networks.as_view()),
    ])),
]