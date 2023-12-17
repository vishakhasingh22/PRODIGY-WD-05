from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'bombay'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid='
    PARAMS = {'units': 'metric'}
    
    API_KEY = ''  # Your API key for Google Custom Search API
    SEARCH_ENGINE_ID = ''  # Your Custom Search Engine ID

    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        # Fetch image data
        data = requests.get(city_url).json()
        search_items = data.get("items")

        # Check if search_items is not empty before accessing elements
        if search_items:
            image_url = search_items[0]['link']
        else:
            image_url = None

        # Fetch weather data
        weather_data = requests.get(url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available in the API')
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred,
            'image_url': None  # Handle the case when search_items is empty
        })
