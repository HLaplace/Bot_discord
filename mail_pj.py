import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import msvcrt

def send_mail(email, subject, file_name, message_text):

	smtp_server = 'smtp.gmail.com'
	port = 465
	mail_sender = 'coucou@gmail.com'
	mail_sender_password = 'password'

	message = MIMEMultipart('alternative')
	message['Subject'] = subject
	message['To'] = email
	message.attach(MIMEText(message_text))
	
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
		server.login(mail_sender, mail_sender_password)
		server.sendmail(mail_sender, email, message.as_string())
		print("send mail : ok")

############################################################################################

while 1:

	mail = input("Recever ? ")
	sujet = input("Subject ? ")
	filename = input("filename ? ")
	texte = input("Body ? ")

	send_mail(mail, sujet, filename, texte)

	print("")
	print("press esc to escape or press any key to contiue : ")
	print("")

	char = msvcrt.getch()
	if char == b'\x1b':
	    os.system('cls')
	    exit()

