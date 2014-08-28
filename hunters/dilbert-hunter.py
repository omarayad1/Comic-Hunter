import requests
from bs4 import BeautifulSoup
import os
import tarfile
import sys

mypath = '../raw-bounties/dilbert'

try:
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
except OSError:
	os.makedirs(mypath)
	onlyfiles = [int(f.split('_')[0]) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
archive = 'http://www.dilbert.com'
link = 'http://www.dilbert.com/1989-04-16/'
html = BeautifulSoup(requests.get(link).content).find(class_='STR_Next')
image_no = 1

while html != None:
	if image_no in onlyfiles:
		html = BeautifulSoup(requests.get(link).content).find(class_='STR_Next')
		image_no += 1
		continue
	image_url = archive + BeautifulSoup(requests.get(link).content).find(class_='STR_Image').find('img')['src']
	image_name = str(image_no).zfill(5) + '_' + image_url.split('/')[-1]
	image = open(mypath + '/' + image_name, 'w')
	image.write(requests.get(image_url).content)
	image.close()
	sys.stdout.write('\r')
	sys.stdout.write('Downloaded Comics: %05d' % image_no)
	sys.stdout.flush()
	link = archive + html['href']
	html = BeautifulSoup(requests.get(link).content).find(class_='STR_Next')
	image_no += 1

tar = tarfile.open("../bounties/dilbert-hunt-bounty.tar.gz", "w:gz")
tar.add("../raw-bounties/dilbert", arcname="dilbert")
tar.close()