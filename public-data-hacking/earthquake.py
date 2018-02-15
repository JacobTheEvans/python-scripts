import urllib2
import csv
import os

def getData(url):
	print("[+] Starting connection...")
	connection = urllib2.urlopen(url)
	print("[+] Connection achieved")
	print("[+] Reading Data...")
	data = connection.read()
	print("[+] Data read returning Info")
	return data

def main():
	earthquakes = []
	data = (getData("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv"))
	#File reader does not work with plain string data type has to be a file object
	f = open("temp.csv","w")
	f.write(data)
	f.close()
	f = open("temp.csv","r")
	for row in csv.DictReader(f):
		time = row["time"]
		place = row["place"]
		mag = row["mag"]
		earthquakes.append("At %s an earthquake occured.\nLocation: %s\nMagnitude: %s" %(time,place,mag))
		
	os.remove("temp.csv")
	for i in earthquakes:
		print i


main()
