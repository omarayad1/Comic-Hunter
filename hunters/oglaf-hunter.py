from bs4 import BeautifulSoup
import requests
import tarfile
import os

mypath = '../raw-bounties/oglaf'

archives = BeautifulSoup(requests.get('http://oglaf.com/archive/').content)
archives = archives.find('div').find('div').find_all('div')[::-1]

links = []

for archive in archives:
	data = archive.find_all('a')[::-1]
	data = ['http://oglaf.com' + x['href'] for x in data]
	links += data

comic_no = 1
for link in links:
	pages = 1
	response = ''
	comic_name = link.split('/')[-2]
	os.makedirs('../raw-bounties/oglaf/' 
		+ str(comic_no).zfill(3) + '_' + comic_name)
	response = requests.get(link + str(pages)).content
	while not (response.find('<center><h1>404 Not Found</h1></center>') + 1):
		image = BeautifulSoup(response).find(class_='content')
		image = requests.get(image.find_all('img')[1]['src']).content
		pic = open('../raw-bounties/oglaf/' 
			+ str(comic_no).zfill(3) + '_' + comic_name + '/' 
			+ comic_name + '_' + str(pages).zfill(2) + '.jpg', 'w')
		pic.write(image)
		pic.close()
		pages += 1
		response = requests.get(link + str(pages)).content
	comic_no += 1
tar = tarfile.open("../bounties/oglaf-hunt-bounty.tar.gz", "w:gz")

tar.add("../raw-bounties/oglaf", arcname="oglaf")

tar.close()