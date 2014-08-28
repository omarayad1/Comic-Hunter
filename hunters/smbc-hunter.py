import requests
from bs4 import BeautifulSoup
import tarfile
import os

archive = 'http://www.smbc-comics.com/archives.php'
archive = BeautifulSoup(requests.get(archive).content).find('div', 
	id='archives')
comics = {}
for link in archive.find_all('font'):
	category = link.find_all_previous('p')[1].string
	try:
		comics[category].append('http://www.smbc-comics.com' 
			+ link.find('a')['href'])
	except:
		comics[category] = ['http://www.smbc-comics.com' 
					+ link.find('a')['href']]
for key, values in comics.iteritems():
	link_no = 1
	comic_type = key.lower().replace(' ', '_')
	try:
		os.makedirs('../raw-bounties/smbc/' + comic_type)
	except:
		pass
	for value in values:
		comic = BeautifulSoup(requests.get(value).content).find(id="comicimage")
		comic_url = comic.find('img')['src']
		comic = requests.get(comic_url).content
		comic_name = comic_url.split('/')[-1]
		image = open('../raw-bounties/smbc/' + comic_type + '/' + str(link_no).zfill(4) + '_' + comic_name, 'w')
		image.write(comic)
		image.close()
		link_no += 1

tar = tarfile.open("../bounties/smbc-hunt-bounty.tar.gz", "w:gz")

tar.add("../raw-bounties/smbc", arcname="smbc")

tar.close()