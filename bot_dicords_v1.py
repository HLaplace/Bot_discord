import requests
from discord.ext import commands

bot = commands.Bot(command_prefix="wtr ", description="Bot_meteo")

@bot.event
async def on_ready():
    print("Connexion : OK")

@bot.command()
async def info(ctx, city):

    # url pour la ville
    adress = 'http://api.openweathermap.org/data/2.5/weather?appid=7eb7eebdc32e8e2def3bb47154c712d3&q='
    url = adress + city

    #requete json
    try:
        json_data = requests.get(url).json()
        info = json_data['weather'][0]['description']
    except KeyError:
        await ctx.send("Je ne trouve pas de ville de ce nom la ")
        pass

    # conversion degre kelvin / celsius
    temp = json_data['main']['temp']
    temp = temp - 273

    # pays
    country = json_data['sys']['country']
    if country == 'FR':
        country = 'France'

    if country == 'US':
        country = 'Etats-Unis'

    if country == 'GB':
        country = 'En dehors de l\Europe'

    #traduction fr
    if info == 'overcast clouds':
        info = 'ciel nuageux'

    if info == 'light rain':
        info = 'pluie légére'

    if info == 'scattered clouds':
        info = 'nuage épars'

    if info == 'broken clouds':
        info = 'nuage bas'

    if info == 'few clouds':
        info = 'ciel dégagé'

    if info == 'clear sky':
        info = 'ciel clair'

    if info == 'moderate rain':
        info = 'Faible pluie'

    await ctx.send('Bulletin météo à ' + str(city) + ", " + str(country))
    await ctx.send(info)
    await ctx.send('Température de ' + str(int(temp)) + '°c')

bot.run(#mettre ici le token du bot) 