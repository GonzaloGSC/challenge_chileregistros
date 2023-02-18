from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path("", include([
        path('seia_data/', views.v_seia_data.as_view()),
    ])),
]