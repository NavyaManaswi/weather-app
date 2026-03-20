from django.shortcuts import render
import requests
import datetime
from django.contrib import messages
from django.conf import settings
# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    # 6bc69b1de2d0ace91d597d8220567867
    # d7ZNHgIr9AjNTRKDB6gaR6UoMVceb-ZrFTYYmIK4Suw
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city= 'gummersbach'    
    WEATHER_API_KEY = settings.OPENWEATHER_API_KEY
    UNSPLASH_KEY = settings.UNSPLASH_API_KEY
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    PARAMS= {'units': 'metric'}

    query = f"{city} skyline"

    url = "https://api.unsplash.com/search/photos"

    params = {
        "query": query,
        "client_id": UNSPLASH_KEY,
        "orientation": "landscape"
    }

    res = requests.get(url, params=params)
    data = res.json()

    results = data.get("results", [])

    if results:
        image_url = results[0]["urls"]["regular"]
    else:
        image_url = "https://dam.destination.one/819700/7f8eb604d54522ffd26daa6d6402474dc311b6eccbed615f54dc43e83e6e111c/innenstadt.jpg"


    try:
            data = requests.get(weather_url,params=PARAMS).json()
            description= data['weather'][0]['description']
            icon= data['weather'][0]['icon']
            temp= data['main']['temp']
            day= datetime.date.today()
            request.session['city'] = city
            timezone_offset = data.get('timezone', 0)
            utc_time = datetime.datetime.utcnow()
            city_time = utc_time + datetime.timedelta(seconds=timezone_offset)
            formatted_time = city_time.strftime("%I:%M %p")

            return render(request,'index.html' , {'description':description , 'icon':icon ,'temp':temp , 'day':day , 'city':city ,'time': formatted_time, 'timezone_offset': timezone_offset,'exception_occurred':False ,'image_url':image_url})

    except:
            
            exception_occurred= True
            messages.error(request,'Entered data is not available to API')
            day=datetime.date.today()
            return render(request,'index.html' ,{'description':'clear sky', 'icon':'01d'  ,'temp':25 , 'day':day , 'city':'Gummersbach' ,'time': 'N/A', 'exception_occurred':exception_occurred } )


        