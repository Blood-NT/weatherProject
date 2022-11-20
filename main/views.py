import urllib.request
import json
from django.shortcuts import render


def index(request):

    if request.method == 'POST':
        city = request.POST['city']
        city = city.replace(" ", "")

        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                        city + '&units=metric&appid=08962508c7447b773da61af9a67694b4').read()
        list_of_data = json.loads(source)
        # if (list_of_data["cod"] == "404"):
        #     data = {
        #         "country_code": "none",
        #         "coordinate": "none",
        #         "temp": "none",
        #         "pressure": "none",
        #         "humidity": "none",
        #         'main': "none",
        #         'description': "none",
        #         'icon': "none",
        #     }
        # else:
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ', '
            + str(list_of_data['coord']['lat']),

            "temp": str(list_of_data['main']['temp']) + ' °C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            'main': str(list_of_data['weather'][0]['main']),
            'description': str(list_of_data['weather'][0]['description']),
            'icon': list_of_data['weather'][0]['icon'],
        }
        print(data)
    else:
        data = {}

    return render(request, "main/index.html", data)

   # "pressure": str(list_of_data['wind']['speed']),
    # "humidity": str(list_of_data['wind']['deg']),
