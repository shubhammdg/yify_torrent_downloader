import requests
from bs4 import BeautifulSoup
import os
import re


def search_results(s):
	movies_res = s.find_all(class_='post-title')
	m_dict = {}
	print("INDEX\tMOVIE")
	for index, movies in enumerate(movies_res[:-9]):
		index+=1
		name = re.search(r'\/">(.*)</a>',str(movies)).groups()[0]
		link = movies.find('a')['href']
		print(str(index)+"\t"+name)
		values = [name, link]
		m_dict[index] = values
	return m_dict


movie = input("Enter Movie Name: ")
page = requests.get("https://yify-movies.fun//?s="+movie)
if "Sorry," in page.text:
	print("Movie not found")
	exit(1)
else:
	print("Movie found")
soup = BeautifulSoup(page.text,'html.parser')
movies_dict = search_results(soup)
movie_select = input("Select a movie from above list: ")
movie_link = movies_dict[int(movie_select)]
movie_page = requests.get(movie_link[1])
soup2 = BeautifulSoup(movie_page.text, 'html.parser')
torrent = soup2.find_all(class_='download-torrent-link')
magnet_link = ""
movie_resolution = input("Enter Movie Resolution (720P or 1080P): ")
flag = 0
for t in torrent:
	if 'magnet' in t['href']:
		if movie_resolution in str(t):
			print (str(t))
			magnet_link = t['href']
			break
		else:
			print(f"Movie not available in {movie_resolution}")
			exit(1)
print("Added movie to Torrent Client")
os.startfile(magnet_link)