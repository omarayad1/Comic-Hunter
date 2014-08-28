import json
import requests
from os import listdir
from os.path import isfile, join
import tarfile

mypath = '../raw-bounties/xkcd'
onlyfiles = [ int(f.split('_')[0]) for f in listdir(mypath) if isfile(join(mypath,f)) ]

comic = 405 if (max(onlyfiles) + 1) == 404 else (max(onlyfiles) + 1)
should_not_contain = '<title>404 - Not Found</title>'
response = requests.get('http://xkcd.com/' + str(comic) + '/info.0.json').content

while not (response.find(should_not_contain) + 1) or comic == 404:
	metadata = json.loads(response)
	if not metadata["link"]:
		url = metadata["img"]
		pic = requests.get(url).content
		file_name = url.split('/')[-1]
		image = open("../raw-bounties/xkcd/" + str(comic).zfill(4) + "_" + file_name, 'w')
		image.write(pic)
		image.close()
	else:
		print "check comic no", comic
		try:
			url = metadata["link"]
			pic_alt = requests.get(requests.get(url).content.split('"')[-1]).content
			pic = requests.get(metadata["img"]).content
			file_name = metadata["img"].split('/')[-1]
			image = open("../raw-bounties/xkcd/" + str(comic).zfill(4) + "_" + file_name, 'w')
			image.write(pic)
			image.close()
			image = open("../raw-bounties/xkcd/" + str(comic).zfill(4) + "_alt_" + file_name, 'w')
			image.write(pic_alt)
			image.close()
		except:
			url = metadata["img"]
			pic = requests.get(url).content
			pic_alt = requests.get(metadata["link"]).content
			file_name = url.split('/')[-1]
			image = open("../raw-bounties/xkcd/" + str(comic).zfill(4) + "_" + file_name, 'w')
			image.write(pic)
			image.close()
			image = open("../raw-bounties/xkcd/" + str(comic).zfill(4) + "_alt_" + file_name, 'w')
			image.write(pic_alt)
			image.close()
	comic += 1
	response = requests.get('http://xkcd.com/' + str(comic) + '/info.0.json').content

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath,f))]
tar = tarfile.open("../bounties/xkcd-hunt-bounty.tar.gz", "w:gz")

for file in onlyfiles:
	tar.add("../raw-bounties/xkcd/" + file, arcname="xkcd/" + file)

tar.close()