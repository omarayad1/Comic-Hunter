import requests
from bs4 import BeautifulSoup
import os
import tarfile
import sys

mypath = '../raw-bounties/three-word-phrase'

try:
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
except OSError:
	os.makedirs(mypath)
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]

archive = 'http://threewordphrase.com/archive.htm'

links = BeautifulSoup(requests.get(archive).content).find('span', class_='links').find_all('a')[::-1]

links = ['http://threewordphrase.com' + link['href'] for link in links]

comic_no = 1

for link in links:
	percent = comic_no / float(len(links)) * 100
	sys.stdout.write('\r')
	sys.stdout.write('Downloaded Comics: %06.2f %%' % percent)
	sys.stdout.flush()
	if comic_no in onlyfiles:
		comic_no += 1
		continue
	img_link = 'http://threewordphrase.com/' +\
		BeautifulSoup(requests.get(link).content)\
		.find('body')\
		.find('div', recursive=False)\
		.find_all('table', recursive=False)[1]\
		.find('img')['src']
	img_name = img_link.split('/')[-1]
	image = open(mypath + '/' + str(comic_no).zfill(3) + '_' + img_name, 'w')
	image.write(requests.get(img_link).content)
	image.close()
	comic_no += 1

tar = tarfile.open("../bounties/three-word-phrase-hunt-bounty.tar.gz", "w:gz")
tar.add("../raw-bounties/three-word-phrase", arcname="three-word-phrase")
tar.close()