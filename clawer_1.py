import requests
from bs4 import BeautifulSoup
import webbrowser

urlBase = "http://www.coolpc.com.tw/phpBB2/"
res = requests.get(urlBase+"portal.php")

targetUTF8 = u'\u9650\u6642' #限時
#filterUTF8 = u'\u8def\u9650'
filterUTF8 = u'\u5df2\u6436\u7562'

soup = BeautifulSoup( res.text)

for divTree in soup.findAll("div", id="center_8"):
	for article in divTree.select('a[href]'):
		if article.text.find(targetUTF8) != -1 & article.text.find(filterUTF8) == -1:
			print article.text
			print urlBase+article['href']
			webbrowser.open(urlBase+article['href'], new=0, autoraise=True)
