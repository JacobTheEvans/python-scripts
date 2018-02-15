import imaplib
import smtplib
import email
import socket
import sqlite3 as db
import os.path
import getpass
import sys
import time
from simplecrypt import encrypt, decrypt
from email.MIMEMultipart import MIMEMultipart
from HTMLParser import HTMLParser
from email.MIMEText import MIMEText

key = "VOD8o5FZRCLGG0L4eQpBRlfUhoLWcGkmuPA3nRBulknbr9N0CR9B9cRghYUw4twFW4NVGNJ48hTH3JIYdfPO21HJmewPkbH9a6K3"

#--Database Functions--

def createDatabase():
	conn = db.connect('emails.db')
	cursor = conn.cursor()
	cursor.execute("create table emails(email text)")

def loadData():
	#Connect to database
	conn = db.connect("emails.db")
	#Load data table
	conn.row_factory = db.Row
	#Open cursor to view
	cursor = conn.cursor()

	#Select all emails and return list
	cursor.execute("select * from emails")
	rows = cursor.fetchall()
	data = []
	for row in rows:
		data.append(("%s") % (row["email"]))
	return data	

def insertData(email):
	conn = db.connect("emails.db")
	cursor = conn.cursor()
	cursor.execute("insert into emails values('%s')" %(email))
	conn.commit()
	conn.close()


def removeData(email):
	conn = db.connect("emails.db")
	cursor = conn.cursor()
	cursor.execute("delete from emails where email='%s'" % (email))
	conn.commit()
	conn.close()
#--End of database functions--

#-- Email functions--
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

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
	msg = email.message_from_string(data[0][1])
	#Disconnect from mailserver
	mailserver.close()

	return strip_tags(str(msg.get_payload()[1]))

def send(username,password,address,subject,text):
	msg = MIMEMultipart()
	msg["From"] = username
	msg["To"] = address
	msg["Subject"] = subject
	msg.attach(MIMEText(text))
	server = smtplib.SMTP('smtp.gmail.com', 25)
	server.ehlo()
	server.starttls() # encrypted
	server.ehlo()
	server.login(username,password)
	server.sendmail(username, address, msg.as_string())
	server.quit()

def forwardloop(username,password):
	temp = ""
	if loadData() == []:
		print("[-] No Emails in Database")
		return
	try:
		print("[+] Starting Server Loop")
		print("<CTRL-C>")
		while True:
			data = read(username,password)
			if temp != data[0]:
				temp = data[0]
				for user in loadData():
					send(username,password,user,"Foward From Server",str(data))
			time.sleep(10)
	except:
		print("[+] Exiting Server Loop")
		return

#--End of email functions--

def usage():
	print("l -start email loop, i -insert new email, r -remove email, p -print users, q -quit,")

def main():
	choice = ""

	#Check if database exists and make sure it is a file 
	if not (os.path.exists("emails.db") and os.path.isfile("emails.db")):
		print("[+] Database created")
		createDatabase()
	print("[+] Welcome to mass email")
	#Option loop for main program
	while choice != "q":

		print("Please input choice")
		choice = raw_input(">> ")

		if choice == "i":
			print("Input Email")
			inputEmail = raw_input("Email: ")
			insertData(inputEmail)

		elif choice == "l":
			print("Input server email")
			inputEmail = raw_input("Email: ")
			print("Input password")
			inputPassword = getpass.getpass()
			forwardloop(inputEmail,inputPassword)

		elif choice =="r":
			print("Input email")
			inputEmail = raw_input("Email: ")
			print("[*] Are you sure you want to remove this email y/n")
			while True:
				areSure = raw_input("y/n: ")
				if(areSure == "y" or areSure == "Y"):
					removeData(inputEmail)
					print("[+] User removed")
					break;
				elif(areSure == "n" or areSure == "N"):
					print("[+] Deletion aborted")
					break
				else:
					print("Not valid input y/n")

		elif choice == "p":
			if(loadData() != []):
				print(("Number of Users: %s") % len(loadData()))
				for userInfo in loadData():
					user = userInfo.split(",")
					print("User: %s,") % (user[0])
			else:
				print("[-] There are no users in database")

		elif choice == "q":
			print("[+] Exiting System")

		elif choice != "":
			usage()


main()