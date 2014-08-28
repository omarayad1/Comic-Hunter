import requests
from bs4 import BeautifulSoup
import os
import tarfile
import sys

mypath = '../raw-bounties/a-softer-world'

try:
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
except OSError:
	os.makedirs(mypath)
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]

archive = 'http://www.asofterworld.com/archive.php'

links = BeautifulSoup(requests.get(archive).content).find_all('a')[1::]
links = [link['href'] for link in links]

comic_no = 1

for link in links:
	percent = comic_no / float(len(links)) * 100
	sys.stdout.write('\r')
	sys.stdout.write('Downloaded Comics: %06.2f %%' % percent)
	sys.stdout.flush()
	if comic_no in onlyfiles:
		comic_no += 1
		continue
	img_link = BeautifulSoup(requests.get(link).content).find('p', id='thecomic').find('img')['src']
	img_name = img_link.split('/')[-1]
	image = open(mypath + '/' + str(comic_no).zfill(4) + '_' + img_name, 'w')
	image.write(requests.get(img_link).content)
	image.close()
	comic_no += 1

tar = tarfile.open("../bounties/a-softer-world-hunt-bounty.tar.gz", "w:gz")
tar.add("../raw-bounties/a-softer-world", arcname="a-softer-world")
tar.close()