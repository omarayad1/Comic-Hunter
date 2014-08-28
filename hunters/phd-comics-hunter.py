import requests
from bs4 import BeautifulSoup
import os
import tarfile
import sys

mypath = '../raw-bounties/phd-comics'

try:
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
except OSError:
	os.makedirs(mypath)
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]

archive = 'http://phdcomics.com/comics/archive_list.php'

comic_page = BeautifulSoup(requests.get(archive).content)

tables = comic_page.find('body')\
	.find_all('table', recursive=False)[1]\
	.find('tr')\
	.find_all('td', recursive=False)[1]\
	.find('center')\
	.find_all('table', recursive=False)[1::]

comic_links = [table.find_all('a') for table in tables]
comic_links = [y['href'] for x in comic_links for y in x]

comic_no = 1

for link in comic_links:
	percent = comic_no / float(len(comic_links)) * 100
	sys.stdout.write('\r')
	sys.stdout.write('Downloaded Comics: %06.2f %%' % percent)
	sys.stdout.flush()
	if comic_no in onlyfiles:
		comic_no += 1
		continue
	img_link = BeautifulSoup(requests.get(link).content).find('img', id='comic')['src']
	img_name = img_link.split('/')[-1]
	image = open(mypath + '/' + str(comic_no).zfill(4) + '_' + img_name, 'w')
	image.write(requests.get(img_link).content)
	image.close()
	comic_no += 1
tar = tarfile.open("../bounties/phd-comics-hunt-bounty.tar.gz", "w:gz")
tar.add("../raw-bounties/phd-comics", arcname="phd-comics")
tar.close()