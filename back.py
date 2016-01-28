from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/visualizer'
db = SQLAlchemy(app)


# create the model
class Get_url(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	url = db.Column(db.String(120), unique=True)

	def __init__(self, url):
		self.url = url

db.create_all()

def create_data():
	url2 = Get_url('alisadammer.com')
	db.session.add(url2)
	db.session.commit()

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
	# create_data()
	app.debug = True
	app.run(host='0.0.0.0')