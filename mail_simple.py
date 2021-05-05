iimport smtplib, ssl
from email.mime.text import MIMEText
import time
import os 
import msvcrt 
from email.mime.multipart import MIMEMultipart

def send_mail(destinataire,subject,message_text):
	
	message = MIMEMultipart()   
	message['To'] = destinataire
	message['Subject'] = subject
	msg = message_text
	message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))
 
	serveur = smtplib.SMTP('smtp.gmail.com', 587)   
	serveur.starttls()   
	serveur.login('hugolapla332@gmail.com', 'Secondairegmail33')   
	texte= message.as_string().encode('utf-8')   
	serveur.sendmail('nom expediteur', message['To'], texte)   
	serveur.quit()   
	print("mail send succesfull")



####################################################################

while 1:

	mail = input("Recever ? ")
	texte = input("Body ? ")
	sujet = input("Subject ? ")
	send_mail(mail,sujet,texte)

	print("")
	print("press esc to escape or press any key to contiue : ")
	print("")
	char = char = msvcrt.getch()
	if char == b'\x1b':
	    os.system('cls')
	    exit()

