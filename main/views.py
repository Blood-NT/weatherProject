import urllib.request
import json
from django.shortcuts import render
import pymongo
from datetime import datetime
import time
from datetime import datetime


def index(request):

    if request.method == 'POST':
        try:
            print("start")
            city = request.POST['city']
            city = city.replace(" ", "")
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                            city + '&units=metric&appid=08962508c7447b773da61af9a67694b4').read()
            list_of_data = json.loads(source)
            # if (list_of_data["cod"] != "200"):
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
                "city": city,
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
            infoDevice = urllib.request.urlopen('http://geolocation-db.com/json/').read()
            infoDevice = json.loads(infoDevice)
            # print(infoDevice)
            now = datetime.now()
            dataSave = {
                "ipv4": infoDevice['IPv4'],
                "city": city,
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ', '
                + str(list_of_data['coord']['lat']),

                "temp": str(list_of_data['main']['temp']) + ' °C',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                'main': str(list_of_data['weather'][0]['main']),
                'description': str(list_of_data['weather'][0]['description']),
                'time': time.time(),
                "date": now.strftime("%d/%m/%Y %H:%M:%S")
            }
            myclient = pymongo.MongoClient("mongodb+srv://nvkien:YiKHbv3Y09jdgKWF@qluser.qf9zv.mongodb.net/profile?retryWrites=true&w=majority")
            mydb = myclient["profile"]
            mycol = mydb["user"]
            x = mycol.insert_one(dataSave)
            infoDevice = urllib.request.urlopen('http://geolocation-db.com/json/').read()
            infoDevice = json.loads(infoDevice)
            history = mycol.find({"ipv4":infoDevice['IPv4']}).sort("time")
            # history = list(reversed(history))
            allData ={
                "data": data,
                "history": history
            }
           
        except:
            allData = {
                "data" : {
                    "city": city,
                    "country_code": "no data",
                    "coordinate": "no data",
                    "temp": "no data",
                    "pressure": "no data",
                    "humidity": "no data",
                    'main': "no data",
                    'description': "no data",
                    'icon': "no data",
                },
                "history":{}
            }
    else:
        myclient = pymongo.MongoClient("mongodb+srv://nvkien:YiKHbv3Y09jdgKWF@qluser.qf9zv.mongodb.net/profile?retryWrites=true&w=majority")
        mydb = myclient["profile"]
        mycol = mydb["user"]
        infoDevice = urllib.request.urlopen('http://geolocation-db.com/json/').read()
        infoDevice = json.loads(infoDevice)
        history = mycol.find({"ipv4":infoDevice['IPv4']}).sort("time",-1)
        print("oke")
        print(type(history))
        # history = list(reversed(history))
        # for x in history:
        #     print(x)
        # print(mydoc)
        # x = mycol.insert_one({"name":"kien"})
        allData = {
            "data": {},
            "history": history
        }
        # infoDevice = urllib.request.urlopen('http://geolocation-db.com/json/').read()

    return render(request, "main/index.html", allData)
