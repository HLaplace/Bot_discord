import requests
import sqlite3
import datetime

print("Programme pour creer un utilisateur :")
name = str(input("nom de l utilisateur : "))
mail = str(input("email de l utilisateur : "))

def execution_SQL(requete):

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()

	result = cursor.execute(requete)

	connection.commit()
	cursor.close()

	return result

def verif_ville(ville_test):

    adress = 'http://api.openweathermap.org/data/2.5/weather?appid=7eb7eebdc32e8e2def3bb47154c712d3&q='
    ville_test = '%20'.join(ville_test.split())
    url = adress + ville_test
    json_data = requests.get(url).json()

    try:
        ville_test = json_data['name']
        print("city name : ok")
        return ville_test

    except KeyError:
        return 0

def city_input():
	city = str(input("ville dont vous voulez la temperaure : "))
	city_test = verif_ville(city)

	if city_test == 0:
		print("Pas de ville de ce nom la")
		city_input()

	else:
		return city_test

def creation_user(prenom, mail, ville, heurecompte):

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()

	data = {'prenom' : prenom, 'mail' : mail, 'ville' : ville, 'heurecompte' : heurecompte}

	result = cursor.execute("""INSERT INTO user_bot (nom_user, email_user, ville_user, heure) 
		VALUES (:prenom, :mail, :ville, :heurecompte)""", data)

	print("utilisateur : " +  " " + str(prenom) + " " +  str(mail) + " " +  str(ville) + " " +  str(heurecompte) + " : creer avec succes")
	connection.commit()
	cursor.close()

	return result

def SELECT_SQL(requete):

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()

	result = cursor.execute(requete)
	result = cursor.fetchall()

	connection.commit()
	cursor.close()

	return result

###############################################################

execution_SQL("""CREATE TABLE IF NOT EXISTS tabtemperature 
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
		id_user INTEGER,
		temperature INTEGER,
		heure INTEGER)""")

execution_SQL("""CREATE TABLE IF NOT EXISTS user_bot
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
		nom_user TEXT,
		email_user TEXT,
		ville_user TEXT,
		heure INTEGER)""")

date = datetime.datetime.now()
heure = date.hour
heure = heure -1
creation_user(name, mail, city_input(), heure)

