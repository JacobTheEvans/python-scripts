import imaplib
import smtplib
import email
from HTMLParser import HTMLParser
from email.parser import HeaderParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys
import getpass

def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

def read(username,password):
	#Connect to Gmail Server
	try:
		mailserver = imaplib.IMAP4_SSL('imap.gmail.com', 993)
	except:
		print("[-] Failed to connect to mailserver")
		sys.exit(0)

	#Login with the given username and password
	try:
		mailserver.login(username,password)
	except:
		print("[-] Failed to login with given credentials")
		sys.exit(0)

	status, count = mailserver.select("Inbox")
	status, data = mailserver.fetch(count[0],'(RFC822)')
	raw_email = data[0][1]
	email_message = (email.message_from_string(raw_email))
	mailserver.close()
	return get_first_text_block(email_message)

def send(username,password,toaddr,subject,message):
	msg = MIMEMultipart()
	msg["From"] = username
	msg["To"] = toaddr
	msg["Subject"] = subject
	text = message
	msg.attach(MIMEText(text))
	server = smtplib.SMTP("smtp.gmail.com",25)
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(username, toaddr, msg.as_string())
	server.quit()

def main():
	print("[+] Welcome to empy.py")
	choice = ""
	try:
		while True:
			print("[*] Input Choice")
			choice = raw_input(">> ")
			if choice == "r":
				print("[+] Please Input Email")
				user = raw_input("Email: ")
				print("[+] Please Input Password")
				sswd = getpass.getpass()
				data = read(user,sswd)
				print("Message: ")
				print data
			elif choice == "s":
				print("[+] Please Input Email")
				user = raw_input("Email: ")
				print("[+] Please Input Password")
				sswd = getpass.getpass()
				print("[+] Please Input Recipients Address")
				addr = raw_input("Address: ")
				print("[+] Please Input Subject")
				sub = raw_input("Subject: ")
				print("[+] Please Input message")
				mes = raw_input(": ")
				send(user,sswd,addr,sub,mes)
			elif choice == "q":
				print("[-] Exiting")
				sys.exit(0)
			else:
				print("r -read, s -send, q -quit")
	except KeyboardInterrupt:
		print("[-] Exiting")

main()