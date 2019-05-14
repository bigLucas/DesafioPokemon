from django.shortcuts import render
from .forms import CityForm
from http import client
import json
import random


def searchPokemonByCity(request):
    aux1 = {}
    pokemon = {}
    returnToHTML = {
        "cidade": "",
        "pais": "",
        "temp": 0,
        "rain": False,
        "pokemon": "",
        "isdigit": False
    }
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            aux1 = request.POST['cidade']
            if not aux1.isdigit():
                conn = client.HTTPSConnection("api.openweathermap.org")
                conn.request(
                    "GET",
                    "/data/2.5/weather?q=%s&units=metric&appid=c798fffbb23738d05f53acef4efd86dd" % aux1)
                r1 = conn.getresponse()
                data1 = r1.read()
                city = json.loads(data1)
                if len(city) < 3:
                    returnToHTML["isdigit"] = True
                    return render(request, 'appPokemon/pesquisa.html', {'form': form, 'returnToHTML': returnToHTML})
                clima = city["weather"][0]["main"]
                temp = city["main"]["temp"]
                returnToHTML["cidade"] = city["name"]
                returnToHTML["pais"] = city["sys"]["country"]
                returnToHTML["temp"] = temp

                if (clima != "Rain") and (clima != "Thunderstorm"):
                    if temp < 5:
                        tipo = "ice"

                    elif (temp >= 5) & (temp < 10):
                        tipo = "water"

                    elif (temp >= 12) & (temp < 15):
                        tipo = "grass"

                    elif (temp >= 15) & (temp < 21):
                        tipo = "ground"

                    elif (temp >= 23) & (temp < 27):
                        tipo = "bug"

                    elif (temp >= 27) & (temp <= 33):
                        tipo = "rock"

                    elif (temp > 33):
                        tipo = "fire"

                    else:
                        tipo = "normal"

                else:
                    tipo = "electric"
                    returnToHTML["rain"] = True

                returnToHTML["tipo"] = tipo
                conn = client.HTTPSConnection("pokeapi.co")
                conn.request("GET", "/api/v2/type/%s" % tipo)
                r1 = conn.getresponse()
                data1 = r1.read()
                user = json.loads(data1)
                pokemon = user['pokemon']
                aux = random.randrange(0, (len(pokemon) - 1))
                returnToHTML["pokemon"] = pokemon[aux]['pokemon']['name']
                conn.close()
                return render(request, 'appPokemon/pesquisa.html', {'form': form, 'returnToHTML': returnToHTML})
            else:
                returnToHTML["isdigit"] = True
                return render(request, 'appPokemon/pesquisa.html', {'form': form, 'returnToHTML': returnToHTML})
    else:
        form = CityForm()
    return render(request, 'appPokemon/pesquisa.html', {'form': form, 'returnToHTML': returnToHTML})
