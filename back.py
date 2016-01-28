from flask import Flask
from flask import render_template
from flask import request
import logging

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
	# ensure the data is stored once
	if request.method == 'POST':
		if request.form['custom-url']:
			logging.debug("Got the url")
	else:
		pass
	return render_template('main.html')

@app.route('/<name>/')
def test(name):
	s = "On this page the main infroamtion about the raw data will be shown "
	t = " The raw data is: %s" 
	return s + '\n' + t % name


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')