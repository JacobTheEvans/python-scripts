from javax.swing import *
from java.awt import *
import urllib2
import re
import sys
import time
import sys

class web:
	def getQuote(self,symbol):
		url = "http://finance.google.com/finance?q="
		content = urllib2.urlopen(url+symbol).read()
		m = re.search('span id="ref.*>(.*)<', content)
		if m:
			quote = m.group(1)
		else:
			quote = "Error"
		return quote

	def getNews(self):
		data = urllib2.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty").read()
		data = self.remove(data,["[","]"," ","\n"])
		ids = data.split(",")
		topStories = []
		for i in range(0,10):
			storie = urllib2.urlopen("https://hacker-news.firebaseio.com/v0/item/" + ids[i] + ".json?print=pretty").read()
			temp = self.remove(storie,["{","}","[","]"]).split("\n")
			titleIndex = 0
			urlIndex = 0
			for x in range(0,len(temp)):
				if "title" in temp[x]:
					titleIndex = x
				if "url" in temp[x]:
					urlIndex = x
			topStories.append(self.remove(temp[titleIndex].split(":")[1],['"',","]) + "$" + (self.remove(temp[urlIndex][10:],['"',","])))
		return topStories

	def remove(self,data,symbols):
		result = data
		for symbol in symbols:
			result = result.replace(symbol,"")
		return result

class display:
	def __init__(self):
		print "[+] Starting"
		self.frame = JFrame("Hacker News")
		self.font = Font("Magneto",Font.BOLD,14)
		self.loadMenu()
		self.loadNewsDisplay()
		self.loadStockDisplay()
		self.update()

	def loadMenu(self):
		self.frame.setSize(800,250)
		self.frame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
		self.frame.setVisible(True)
		self.frame.setLayout(BorderLayout())

	def loadNewsDisplay(self):
		self.news = JPanel()
		self.news.setBackground(Color.decode("#0A0A33"))
		self.news.setLayout((BorderLayout()))
		self.label = JLabel(" " * 65 + "News")
		self.label.setFont(self.font)
		self.label.setForeground(Color.decode("#FCFCFC"))
		self.news.add(self.label,BorderLayout.NORTH)
		self.newsList = DefaultListModel()
		self.content = JList(self.newsList)
		self.content.setBackground(Color.decode("#0A0A33"))
		self.content.setForeground(Color.decode("#FCFCFC"))
		self.content.setFont(self.font)
		self.content.setSelectionBackground(Color.decode("#0A0A33"))
		self.content.setSelectionForeground(Color.decode("#FCFCFC"))
		self.news.add(self.content, BorderLayout.CENTER)
		self.frame.add(self.news,BorderLayout.CENTER)
		self.updateNews()

	def loadStockDisplay(self):
		self.display = JPanel()
		self.display.setLayout(BorderLayout())
		self.display.setBackground(Color.decode("#0A0A33"))
		self.display.setBorder(BorderFactory.createMatteBorder(0,3,0,0,Color.decode("#8080E6")))
		self.label = JLabel(" Stocks")
		self.label.setForeground(Color.decode("#FCFCFC"))
		self.label.setFont(self.font)
		self.display.add(self.label,BorderLayout.NORTH)
		self.stocks = DefaultListModel();
		self.stockDisplay = JList(self.stocks)
		self.stockDisplay.setBackground(Color.decode("#0A0A33"))
		self.stockDisplay.setForeground(Color.decode("#FCFCFC"))
		self.stockDisplay.setFont(self.font)
		self.stockDisplay.setSelectionBackground(Color.decode("#0A0A33"))
		self.stockDisplay.setSelectionForeground(Color.decode("#FCFCFC"))
		self.display.add(self.stockDisplay, BorderLayout.CENTER)
		self.frame.add(self.display,BorderLayout.EAST)
		self.updateStocks()

	def updateStocks(self):
		companys = ["MSFT","SNDK","GOOGL","NOK","EMC","HPQ","IBM","EBAY","AAPL","AMZN"]
		tempList = []
		for company in companys:
			Quote = web()
			tempList.append(company + " " + str(Quote.getQuote(company)))
		self.stocks.clear()
		for item in tempList:
			self.stocks.addElement(item)
		self.stocks.addElement("ENDLIST")
		print self.stocks
		print("[+] Stocks update")

	def updateNews(self):
		news = web()
		self.newsList.clear()
		stories = news.getNews()
		for s in stories:
			self.newsList.addElement(s.split("$")[0])



	def update(self):
		while True:
			print("In loop")
			self.updateStocks()
			self.stocks.addElement("update")
			self.stocks.setSelectedIndex(0)
			self.updateNews()
			time.sleep(3)


display()
