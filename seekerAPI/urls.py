from django.urls import path, include
from seekerAPI import views

urlpatterns = [
    path('', views.SeekView.as_view())
]
