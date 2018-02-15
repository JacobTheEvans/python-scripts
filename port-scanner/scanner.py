import optparse
import socket
from socket import *
from threading import *

screenLock = Semaphore(value=1)

def connScan(tgtHost,tgtPort):
	try:
		connSkt = socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tgtHost,tgtPort))
		connSkt.send("Test")
		results = connskt.recv(100)
		screenLock.acqurie()
		print("[+]%d/tcp open" % tgtPort)
		print("[+] " + str(results))
	except:
		screenLock.acquire()
		print("[-]%d/tcp closed"% tgtPort)
	finally:
		screenLock.release()
		connSkt.close()

def portScan(tgtHost,tgtPorts):
	try:
		tgtIP = gethostbyname(tgtHost)
	except:
		print("[-] Cannot resolve '%s': Unkown host"% tgtHost)
		return
	try:
		tgtName = gethostbyaddr(tgtIP)
		print("[+] Scan Results for: " + tgtName[0])
	except:
		print("[+] Scan Results for: " + tgtIP)
	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		print("Scanning port " + str(tgtPort))
		connScan(tgtHost,int(tgtPort))

def main():
	parser = optparse.OptionParser("Usage scanner.py -H " +\
			"<targest host> -m <max range of ports> -p <target port>")
	parser.add_option("-H", dest="tgtHost",type="string", \
					help="specify target host")
	parser.add_option("-p",dest="tgtPort",type="string", \
					help="specify target port")
	parser.add_option("-m",dest="max",type="string", \
					help="max range of ports to scan")
	(options, args) = parser.parse_args()
	tgtHost = options.tgtHost
	tgtPorts = str(options.tgtPort).split(',')
	tgtMax = options.max

	if(tgtHost == None):
		print(parser.usage)
		exit(0)
	if((tgtPorts[0] == 'None') and (tgtMax == None)):
		print("Error: Must provide specific ports or a max")
		print(parser.usage)
		exit(0)
	if((tgtMax != None) and (tgtPorts[0] != "None")):
		print("Error: Cannot have range and specific ports")
		print(parser.usage)
		exit(0)
	if(tgtPorts[0] != 'None'):	
		portScan(tgtHost, tgtPorts)
	else:
		tgtPorts = range(int(tgtMax)+1)
		portScan(tgtHost,tgtPorts)

if __name__ =="__main__":
	main()