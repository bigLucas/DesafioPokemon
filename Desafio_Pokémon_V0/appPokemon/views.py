from django.shortcuts import render
from .forms import CityForm
import requests
import random


def searchPokemonByCity(request):
    user = {}
    city = {}
    aux1 = {}
    pokemon = {}
    returnToHTML = {
        "cidade": "",
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
                url = 'https://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=c798fffbb23738d05f53acef4efd86dd' % aux1
                response = requests.get(url)
                city = response.json()
                clima = city['weather'][0]['main']
                temp = city["main"]["temp"]
                returnToHTML["cidade"] = city["name"]
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
                        tipo = "stone"

                    elif (temp > 33):
                        tipo = "fire"

                    else:
                        tipo = "normal"

                else:
                    tipo = "electric"
                    returnToHTML["rain"] = True

                returnToHTML["tipo"] = tipo
                url = 'https://pokeapi.co/api/v2/type/%s' % tipo
                response = requests.get(url)
                # pokemon = response.json()
                user = response.json()
                pokemon = user['pokemon']
                aux = random.randrange(0, (len(pokemon) - 1))
                returnToHTML["pokemon"] = pokemon[aux]['pokemon']['name']
                return render(request, 'appPokemon/pesquisa.html', {'form': form, 'returnToHTML': returnToHTML})
            else:
                returnToHTML["isdigit"] = True
                return render(request, 'appPokemon/pesquisa.html', {'form': form, 'returnToHTML': returnToHTML})
    else:
        form = CityForm()
    return render(request, 'appPokemon/pesquisa.html', {'form': form, 'returnToHTML': returnToHTML})
