# Code utilisant l'api meteo openweather et renvoyant la meteo dans une ville donne avec la commande 
# wtr info nomdelaville

import requests
from discord.ext import commands

bot = commands.Bot(command_prefix="wtr ", description="Bot meteo pour discord")

@bot.event
async def on_ready():
    print("Connexion : OK")
    print("")

@bot.command()
async def info(ctx, city):

    # url pour la ville
    adress = 'http://api.openweathermap.org/data/2.5/weather?appid=7eb7eebdc32e8e2def3bb47154c712d3&q='
    url = adress + city

    #requete json
    print("Recherche info: " + str(city))

    try:
        #requete principal
        json_data = requests.get(url).json()
        info = json_data['weather'][0]['description']

        # conversion degre kelvin / celsius
        temp = json_data['main']['temp']
        temp = temp - 273
        print("Recherche info: " + str(city) + " : OK")
        
        # pays
        country = json_data['sys']['country']

        pays = [['FR','US','GB'], ['France','Etats-Unis','Royaume-Uni']]

        for i in range (0,len(pays[0])):
            if country == pays[0][i]:
                country = pays[1][i]

        # traduction fr
        traduction = [['overcast clouds','light rain','scattered clouds','broken clouds','few clouds','clear sky','moderate rain'],
                ['ciel nuageux','pluie légére','nuage épars','nuage bas','ciel dégagé','ciel clair','Faible pluie']]

        for i in range (0,len(traduction[0])):
            if info == traduction[0][i]:
                info = traduction[1][i]

        await ctx.send('Bulletin météo à ' + str(city) + ", " + str(country))
        await ctx.send(info)
        await ctx.send('Température de ' + str(int(temp)) + '°c')

    except KeyError:
        await ctx.send("Je ne trouve pas de ville de ce nom la ")
        print("Recherche info: " + str(city) + " : ville inconnu")
        pass
    print("")

bot.run(#mettre ici le token du bot)
