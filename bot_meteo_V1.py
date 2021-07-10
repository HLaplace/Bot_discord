#####################################################################
#Avant le lancement il faut changer les parametres d envoie de mail et la cle de l api
#####################################################################
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import os
import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import datetime
date = datetime.datetime.now()
import threading

#######################################################################################
# requete de recuperation / conversion de la temperature
def requete(city_name):

	adress = 'http://api.openweathermap.org/data/2.5/weather?appid=7eb7eebdc32e8e2def3bb47154c712d3&q='
	city_name = '%20'.join(city_name.split())
	url = adress + city_name

    #requete principal
	json_data = requests.get(url).json()
	temp = json_data['main']['temp']
	temp = temp - 272.15
	temp = int(temp)

	return temp

# requete d ajout de donnes dans la base de donne prenant en parametre la temperature et l heure
def add_database(id_utilisateur, temp_actuelle):

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()

	cursor.execute("""CREATE TABLE IF NOT EXISTS tabtemperature 
		(id INTEGER PRIMARY KEY AUTOINCREMENT ,
		id_user INTEGER,
		temperature INTEGER,
		heure INTEGER)""")

	date = datetime.datetime.now()

	data = {"id_user" : id_utilisateur, "temperature" : temp_actuelle, "heure" : date.hour}

	cursor.execute("""INSERT INTO tabtemperature (id_user, temperature, heure) VALUES (:id_user ,:temperature , :heure)""", data)
	
	print("Temperature a " + str(date.hour) + "h de " + str(temp_actuelle) + " c.")

	connection.commit()
	cursor.close()

# fonction d envoi de mail
def send_mail(file_name):

	USER = selection_item_user(i)

	# parite a modifier
	smtp_server = 'smtp.gmail.com'
	port = 465
	expediteur = # email as str
	password = # password as str desable gmail security
	##############################################

	message = MIMEMultipart('alternative')
	message['Subject'] = 'Temperature du jour'
	message['From'] = 'noreply@meteo.fr'
	message['To'] = USER[0][2] 	

	date = datetime.datetime.now()
	message.attach(MIMEText("Bonjour, " + str(USER[0][1]) + " veuillez trouvez ci joint le suivi des temperatures du "
		+ str(date.day) + " / " + str(date.month) + " / " + str(date.year) + ' a ' + str(USER[0][3]) +".", 'plain'))
	
	with open(file_name, 'rb') as attachment:
		file_part = MIMEBase('application', 'octet-stream')
		file_part.set_payload(attachment.read())
		encoders.encode_base64(file_part)
		file_part.add_header(
		'Content-Disposition',
		'attachment; filename='+ str(file_name)
		)
		message.attach(file_part)

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(expediteur, password)
		server.sendmail(message['From'], message['To'], message.as_string())
		print("send mail : ok")

# fonction pour executer une requete sql mise en parametre
def execution_SQL(requete):

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()

	result = cursor.execute(requete)

	connection.commit()
	cursor.close()

	return result

# fonction pour executer une requete sql SELECT mise en parametre
def SELECT_SQL(requete):

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()

	result = cursor.execute(requete)
	result = cursor.fetchall()

	connection.commit()
	cursor.close()

	return result

# foction pour creer la courbe
def courbe(heure, tab_temperature, file_number):

	temp = heure
	tab = []
	for i in range (heure, 24):#24
		tab.append(i)

	for j in range(0,heure):
		tab.append(j)
	print("legende en x : " + str(tab))
	
	fig,ax = plt.subplots()
	plt.plot([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], tab_temperature)
	plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
	ax.set_xticklabels(tab, fontsize=7)
	plt.grid(True)
	#plt.show()
	
	file_name_exit = 'graphe' + str(file_number) + ".png"
	print("file save as : " +str(file_name_exit))
	plt.savefig(file_name_exit)  
	plt.clf()  
	
	return file_name_exit 

# fonction recuperant les donnes dans la bdd pour creer la courbe
def requete_courbe(requete, indice):

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()


	data = {'var_suivi' : indice}

	result = cursor.execute(requete, data)
	result = cursor.fetchall()

	connection.commit()
	cursor.close()

	return result

# fonction selectionnant tt les valeurs d un utilisateur
def selection_item_user(var_suivi):

	data = {"var_suivi" : var_suivi}

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()
	result = cursor.execute("""SELECT * FROM user_bot where id = :var_suivi""", data)
	result = cursor.fetchall()

	connection.commit()
	cursor.close()

	return result

# fonction pour supprimer tout les valeurs de temperature apres envoi du mail
def delete_item(var_suivi):

	connection = sqlite3.connect('bot_meteo.db')
	cursor = connection.cursor()

	data = {'var_suivi' : var_suivi}
	result = cursor.execute("""DELETE FROM tabtemperature where id_user = :var_suivi""", data )

	connection.commit()
	cursor.close()

def main():
	# coeur du programme
	j = 0
	hour = 0
	while 1:
		print("####################################################################")
		# la boucle for est execute tout les heures
		date = datetime.datetime.now()
		print(date.hour)
		for i in range (1, (nbre_user + 1)):

			# recuperation de l heure de l envoie du mail pour l utilisateur d id I dans la bdd
			heure =  selection_item_user(i)[0][4]

			USER_temp = selection_item_user(i) # regarder dans la bdd si 0 ets l'urtilisateur 1
			temperature_actuel = requete(USER_temp[0][3])
			add_database(i, temperature_actuel) 
			print("Pour l utilisateur " + str(USER_temp[0][1]) +" "+ str(USER_temp[0][2]) + " "+str(USER_temp[0][3]))
			print(" ")

			# si c l heure de l envoie du mail
			if date.hour == heure: 

				# valeur servant a la creation de la courbe
				#print("requete heure : " + str(requete_courbe("""SELECT heure FROM tabtemperature where id_user = :var_suivi""", i)))
				temperature_coube = requete_courbe("""SELECT temperature FROM tabtemperature where id_user = :var_suivi""", i)
				print("temperature courbe : " +str(temperature_coube))

				#creation de la courbe et envoie du mail 
				send_mail(courbe(heure,temperature_coube, j))
				delete_item(i)
				j = j + 1 

			# cas ou ce n est pas l heure de l envoie du mail
			else:
				print("else")
				pass

		print("####################################################################")
		print("")
		time.sleep(delai)

###########################################################################################
# creation des differents utilisateur DE TEST	 
#creation_user('Hugo', 'hugolaplace33@gmail.com', 'Bordeaux', 23)
#creation_user('Hugo Laplace', 'hugolaplace33@gmail.com', 'paris', date.hour - 1)
# IL EST TRES IMPORTANT DE CREER LES UTILISATEUR QU UNE SEUL FOIS

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

# denombrage du nombre d utilisateur
nbre_user = SELECT_SQL("""SELECT COUNT (*) FROM user_bot""")
nbre_user = nbre_user[0][0]
print("nombre d utilisateur : " + str(nbre_user))

# Cas ou la bdd est vide (il n'y a pas d'utilisateur)
if nbre_user == 0:
	print ("FATAL ERROR : NO USER")
	cmd = 'python creation_bdd.py'
	os.system(cmd)

	# denombrage du nombre d utilisateur
	nbre_user = SELECT_SQL("""SELECT COUNT (*) FROM user_bot""")
	nbre_user = nbre_user[0][0]
	print("nombre d utilisateur : " + str(nbre_user))

###########################################################################################

print(" ")
delai = int(input("delai : ")) # delai = 3600 (nombres de secondes dans une heure)
print(" ")
j = 0 # cette variable est le numero du graphe a creer

# suppresion de toute les donnes de temperature de la bdd
for i in range (1, (nbre_user + 1)):
	delete_item(i)

# synchronisation a l heure pile (presicion minutes)
debut = int(input("min de depart : "))
date = datetime.datetime.now()
while date.minute != debut:
	time.sleep(1)
	date = datetime.datetime.now()

# debut du programme
print("debut programme : ")
print(datetime.datetime.now())
print(" ")

# coeur du programme
#th1 = threading.Thread(target=main)

#th1.start()
#th1.join()
main()	
