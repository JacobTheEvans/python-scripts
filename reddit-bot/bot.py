import praw
from lxml import html
import requests
import xml.etree.ElementTree

DOMAIN = "amazon"

def scrape(url):
	page = requests.get(url)
	tree = html.fromstring(page.text)
	#Prodcut name
	name = tree.xpath('//span[@id="productTitle"]/text()')
	#Price of product
	price = tree.xpath('//span[@id="priceblock_ourprice"]/text()')
	#Average Rating does not have specific id
	#So a simple for loop of span tags is used
	raw_span = tree.xpath('//span/text()')
	for item in raw_span:
		if "out of" in item:
			rating = item
	return("Product Name: %s\nProudct Price: %s USD\nAverage Rating: %s" %(name[-1],price[-1],rating.replace("\n","")[4:]))

def run_bot(connection):
	 subreddit = connection.get_subreddit("test")
	 comments = subreddit.get_comments(limit=25)
	 for comment in comments:
	 	comment_text = comment.body
	 	if(DOMAIN in comment_text):
	 		data = comment_text.split(" ")
	 		print(data)
	 		for item in data:
	 			if(DOMAIN in item):
	 				comment.reply(scrape(item) + "\nThis is an automated response to an amazon link.")

def connect_to_reddit():
	connection = praw.Reddit(user_agent = "A bot that will go to an amazon link and reply the name, price, number of stars")
	connection.login("username","password")
	run_bot(connection)

connect_to_reddit()