import urllib2, htmllib, formatter, re, sys

def usage():
	print("crawler.py [URL] [Max number of links] [Output file]")

def crawl(url):
	if "http" not in url:
		try:
			content = urllib2.urlopen("http://"+url)
		except urllib2.URLError:
			return []
	else:
		try:
			content = urllib2.urlopen(url)
		except urllib2.HTTPError:
			return []
	data = content.read()
	content.close()
	dataForamt = formatter.AbstractFormatter(formatter.NullWriter())
	htmlText = htmllib.HTMLParser(dataForamt)
	htmlText.feed(data)
	links = htmlText.anchorlist
	return links

def main(argv):
	print("Crawler is starting...")
	links = [argv[0]]
	data = [argv[0]]
	while len(links) != 0 and len(data) < int(argv[1]):
		URL = links[len(links)-1]
		del links[len(links)-1]
		htmlLinks = crawl(URL)
		for i in htmlLinks:
			if i not in data:
				links.append(i)
				data.append(i)
	print("Crawler is finshed")
	result = ""
	for i in data:
		result += "\n" + i
	try:
		f = open(argv[2],"w")
		f.write(result)
	except IOError:
		print("Error opening file")

if __name__ == "__main__":
	if len(sys.argv) < 4 or len(sys.argv) > 4:
		usage()
	elif len(sys.argv) == 4:
		main(sys.argv[1:])