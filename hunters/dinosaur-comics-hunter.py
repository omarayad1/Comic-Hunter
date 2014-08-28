from bs4 import BeautifulSoup
import requests
from os import listdir
from os.path import isfile, join
import tarfile

mypath = '../raw-bounties/dinosaur-comics'
onlyfiles = [int(f.split('_')[0]) for f in listdir(mypath) if isfile(join(mypath,f))]

archive = requests.get('http://www.qwantz.com/archive.php').content

archive_html = BeautifulSoup(archive)

archives = archive_html.find_all('ul', class_='archive')[::-1]

links = []

for archive in archives:
	data = archive.find_all('a')[::-1]
	data = [x['href'] for x in data]
	links += data
link_no = 1
for link in links:
	if link_no in onlyfiles:
		link_no += 1
		continue
	if link.find('www.qwantz.com') + 1:
		comic_link = BeautifulSoup(requests.get(link).content).find(class_="comic")['src']
		comic_name = comic_link.split('=')[-1].split('/')[-1]
		comic = requests.get(comic_link).content
		image = open('../raw-bounties/dinosaur-comics/' + str(link_no).zfill(4) + '_' + comic_name, 'w')
		image.write(comic)
		image.close()
		link_no += 1


onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath,f))]
tar = tarfile.open("../bounties/dinosaur-comics-hunt-bounty.tar.gz", "w:gz")

for file in onlyfiles:
	tar.add("../raw-bounties/dinosaur-comics/" + file, arcname="dinosaur-comics/" + file)

tar.close()