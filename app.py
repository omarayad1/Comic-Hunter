from flask import Flask
import dropbox

DROPBOX_APP_KEY = 'b0a5yq7r0oghtqf'
DROPBOX_APP_SECRET = 't635eukfp475d9t'
DROPBOX_ACCESS_TOKEN = 'nRa2x_3N2_wAAAAAAAASj0NxGFZkMInoVa2Id3FM34HjcQd2wSbTFsHKInjMZgSI'

app = Flask(__name__, static_url_path='.')

@app.route("/")
def root():
	client = dropbox.client.DropboxClient(DROPBOX_ACCESS_TOKEN)
	file = client.get_file('/xkcd-hunt-bounty.tar.gz')
	return file