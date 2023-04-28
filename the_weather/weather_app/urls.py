from django.urls import path
from . import views
from weather_app.views import weather, autocomplete
  # Import the views from the current app

urlpatterns = [
    path('', views.weather, name='weather'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('city_suggestions/', views.city_suggestions, name='city_suggestions'),
    
]
