import os
import configparser
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django import forms
import requests
from geopy.geocoders import Nominatim
from ipware import get_client_ip
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .autocomplete import trie
from .autocomplete import get_city_suggestions
import os
import configparser

class CityForm(forms.Form):
    city = forms.ChoiceField(choices=[('London', 'London'), ('New York', 'New York'), ('Tokyo', 'Tokyo')])


@api_view(['GET'])
def autocomplete(request):
    query = request.GET.get('q', '').lower()
    suggestions = trie.suggestions(query)
    return JsonResponse({'suggestions': suggestions})



def city_suggestions(request):
    if request.method == 'GET':
        prefix = request.GET.get('prefix', '')
        suggestions = get_city_suggestions(prefix)
        return JsonResponse({'suggestions': suggestions})
    return HttpResponseNotAllowed(['GET'])

def get_location(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        return 'London'  # Fallback to London if IP not found

    ip_api_url = f"http://ip-api.com/json/{client_ip}"
    ip_api_response = requests.get(ip_api_url)
    ip_data = ip_api_response.json()

    lat = ip_data.get('lat')
    lon = ip_data.get('lon')

    if lat is None or lon is None:
        return 'London'  # Fallback to London if latitude or longitude not found

    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.reverse(f"{lat}, {lon}")
    return location.raw['address']['city']


def weather(request):
    

    #api_key = os.environ['WEATHER_API_KEY']
    
    
    
    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    key_ini_path = os.path.join(current_dir_path, 'key.ini')

    config = configparser.ConfigParser()
    config.read(key_ini_path)
  
    api_key = config.get('API', 'WEATHER_API_KEY', fallback=None)
    
    

    
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    city = "London"

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
    else:
        form = CityForm()
        city = get_location(request)

    response = requests.get(url.format(city, api_key))
    data = response.json()

    context = {
        'city': city,
        'temperature': round(data['main']['temp'] - 273.15),  
        'description': data['weather'][0]['description'],
        'form': form
    }

    return render(request, 'weather_app/weather.html', context)


    