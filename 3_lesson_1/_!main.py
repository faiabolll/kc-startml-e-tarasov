# 1. Цепочка вызовов

import sqlite3
from bs4 import BeautifulSoup
import requests, hashlib
from io import open as iopen
# Старое название библиотеки
from urllib.parse import urlsplit, unquote

class Database:
	def __init__(self, dbname='anime.db'):
		self.con = sqlite3.connect(dbname)
		self.cur = self.con.cursor()
		
	def select_data(self, query):
		return self.cur.execute(query)

	def insert_data(self, query):
		self.cur.execute(query).commit()

	def __exit__(self):
		self.cur.close()
		self.con.close()

def parse_image_url(url):
	html_doc = requests.get(url).text
	soup = BeautifulSoup(html_doc, 'html.parser')
	img_container = soup.find(class_='postContainer')
	# [1] - нужно выбирать только второй элемент
	img_path = img_container.find_all('img')[1]
	img_url = 'https:' + img_path.get('src')
	requests_image(img_url)

def requests_image(img_url):
	suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg',]
	file_name =  unquote(urlsplit(img_url)[2].split('/')[-1])
	resp = requests.get(img_url)
	file_suffix = file_name.split('.')[1]
	if file_suffix in suffix_list and resp.status_code == requests.codes.ok:
		with iopen(file_name, 'wb') as file:
			file.write(resp.content)
	
		# Проверить целостность изображений
		hash = hashlib.md5()
		blocksize = 2**16
		with open(file_name, "rb") as f:
			for block in iter(lambda: f.read(blocksize), b""):
				hash.update(block)
		check_sum = hash.hexdigest()

		# Занесение в БД
		if database.select_data("SELECT * FROM sums WHERE sum = '%s'" % check_sum) is None:
			database.insert_data("INSERT INTO sums VALUES (%s)" % check_sum)	

def main():
	global database
	database = Database()
	
	Anime_types = ['http://anime.reactor.cc/tag/Anime+%D0%9D%D1%8F%D1%88%D0%B8', 'http://anime.reactor.cc/tag/Anime+Cosplay', 'http://anime.reactor.cc/tag/Anime+%D0%9A%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B', 'http://anime.reactor.cc/tag/Anime+Art']
	for x in Anime_types:
		parse_image_url(x)
		
if __name__ == "__main__":
	main()