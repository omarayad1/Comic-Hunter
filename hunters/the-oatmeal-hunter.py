import requests
from bs4 import BeautifulSoup
import os
import tarfile
import sys

page = 1
archive = 'http://theoatmeal.com/comics_pg/page:'

current_response = requests.get(archive + str(page)).content
prev_response = ''
links = []
downloaded_comics = [int(name.split('_')[0]) for name in os.listdir("../raw-bounties/the-oatmeal/")]
while current_response != prev_response:
	prev_response = current_response
	links_temp = BeautifulSoup(prev_response).find_all('a', class_='arrow_right')
	links_temp = ['http://theoatmeal.com' + link['href'] for link in links_temp if link['href'].find('/comics/') + 1]
	links += links_temp
	page += 1
	current_response = requests.get(archive + str(page)).content
comic_no = 1
for link in links[::-1]:
	sys.stdout.write('\r')
	sys.stdout.write(str(comic_no/float(len(links)) * 100) + ' %')
	sys.stdout.flush()
	if comic_no in downloaded_comics:
		comic_no += 1
		continue
	comic_name = link.split('/')[-1]
	comic_images = BeautifulSoup(requests.get(link).content)
	comic_images = comic_images.find('div', id='comic')
	comic_images.find('div', id='content_footer2').extract()
	comic_images = comic_images.find_all('img')
	image_no = 1
	current_dir = '../raw-bounties/the-oatmeal/' + str(comic_no).zfill(3) + '_' + comic_name
	try:
		os.makedirs(current_dir)
	except:
		pass
	for comic_image in comic_images:
		file_name = comic_image['src'].split('/')[-1]
		comic = requests.get(comic_image['src']).content
		image = open(current_dir + '/' + str(image_no).zfill(2) + '_' + file_name, 'w')
		image.write(comic)
		image.close()
		image_no += 1
	comic_no += 1

tar = tarfile.open("../bounties/the-oatmeal-hunt-bounty.tar.gz", "w:gz")

tar.add("../raw-bounties/the-oatmeal", arcname="the-oatmeal")

tar.close()
