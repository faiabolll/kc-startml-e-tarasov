import sqlite3
from bs4 import BeautifulSoup
import requests, hashlib
from io import open as iopen
from urlparse import urlsplit

def md5sum(filename, blocksize=65536):
	hash = hashlib.md5()
	with open(filename, "rb") as f:
		for block in iter(lambda: f.read(blocksize), b""):
			hash.update(block)
	return hash.hexdigest()

def parse_image_url(url):
	html_doc = requests.get(url).text
	soup = BeautifulSoup(html_doc, 'html.parser')
	first = soup.find(class_='postContainer')
	two = first.find_all('img')
	requests_image(two[1].get('src'))

def unic_check(file_name):
	check_sum = md5sum(file_name)
	if c.execute("SELECT * FROM sums WHERE sum = '%s'" % check_sum) != None:
		cur.close()
		conn.close()
		return
	else:
		c.execute("INSERT INTO sums VALUES (%s)" % check_sum)
		c.commit()
		cur.close()
		conn.close()
		return

def requests_image(file_url):
	suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg',]
	file_name =  urlsplit(file_url)[2].split('/')[-1]
	file_suffix = file_name.split('.')[1]
	i = requests.get(file_url)
	if file_suffix in suffix_list and i.status_code == requests.codes.ok:
		with iopen(file_name, 'wb') as file:
			file.write(i.content)
	else:
		return False
	unic_check(file_name)

def main():
	Anime_types = ['http://anime.reactor.cc/tag/Anime+%D0%9D%D1%8F%D1%88%D0%B8', 'http://anime.reactor.cc/tag/Anime+Cosplay', 'http://anime.reactor.cc/tag/Anime+%D0%9A%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B', 'http://anime.reactor.cc/tag/Anime+Art']
	global conn
	global c
	conn = sqlite3.connect('anime.db')
	c = conn.cursor()
	for x in Anime_types:
		parse_image_url(x)
		
if __name__ == "__main__":
	main()