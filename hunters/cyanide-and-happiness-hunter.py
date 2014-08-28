import requests
from bs4 import BeautifulSoup
import sys
import tarfile
import os

mypath = '../raw-bounties/cyanide-and-happiness'
try:
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
except OSError:
	os.makedirs(mypath)
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
archive = 'http://explosm.net/comics/archive/'

year_selector = '#maincontent'

archive_html = BeautifulSoup(requests.get(archive).content)

years = archive_html.select(year_selector)[0].find_all('div')[1]
years = [archive + year.string + '/' for year in years.find_all(['a', 'b'])]
comic_links = []
for year in years:
	year_comics = BeautifulSoup(requests.get(year).content).find('table')
	year_comics = ['http://explosm.net' + comic['href'] for comic in year_comics.find_all('a')]
	comic_links += year_comics
comic_no = 1

for link in comic_links:
	percent = comic_no / float(len(comic_links)) * 100
	sys.stdout.write('\r')
	sys.stdout.write('Downloaded Comics: %06.2f %%' % percent)
	sys.stdout.flush()
	if comic_no in onlyfiles:
		comic_no += 1
		continue
	comic_page = BeautifulSoup(requests.get(link).content)
	image_link = comic_page.select('#maincontent')[0].find_all('div')
	try:
		comic_link = image_link[2].find_all('div')[0].find_all('img')[0]['src']
	except IndexError:
		try:
			comic_link = image_link[2].find_all('div')[0].find_all('embed')[0]['src']
		except IndexError:
			comic_no += 1
			continue
	if not (comic_link.find('explosm.net') + 1):
		comic_link = 'http://explosm.net' + comic_link 
	comic_name = str(comic_no).zfill(4) + '_' + comic_link.split('/')[-1]
	comic = open('../raw-bounties/cyanide-and-happiness/' + comic_name, 'w')
	comic.write(requests.get(comic_link).content)
	comic.close()
	comic_no += 1
tar = tarfile.open("../bounties/cyanide-and-happiness-hunt-bounty.tar.gz", "w:gz")

tar.add("../raw-bounties/cyanide-and-happiness", arcname="cyanide-and-happiness")

tar.close()