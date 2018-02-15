# -*- coding: utf-8 -*-

import urllib2
import xml.etree.ElementTree as ET

#Using api.openweathermap.org
#http://api.openweathermap.org/data/2.5/weather?q=vernal,ut&mode=xml

def getHTML(url):
	connection = urllib2.urlopen(url)
	data = connection.read()
	return data

def parseData():
	data = getHTML("http://api.openweathermap.org/data/2.5/weather?q=vernal,ut&mode=xml")
	root = ET.fromstring(data)
	city = (root.find("city")).attrib["name"]
	temp = str(float(root.find("temperature").attrib["value"]) - 273) + " °c"
	hum = root.find("humidity").attrib["value"] + root.find("humidity").attrib["unit"]
	clouds = root.find("clouds").attrib["name"]
	prec = root.find("precipitation").attrib["mode"]
	if "no" in prec:
		prec = "No"
	elif "yes" in prec:
		prec = "Yes"
	return("City: %s,\nTemperature: %s,\nPrecipitation: %s,\nHumidity: %s,\nClouds: %s" %(city,temp,prec,hum,clouds))

def main():
	print(parseData())

main()