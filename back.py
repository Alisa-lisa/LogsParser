from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/visualizer'
db = SQLAlchemy(app)
app.secret_key = 'f43fee5tbt'

# create the model
class Url(db.Model):
	__tablename__ = 'url_counter'
	id = db.Column(db.Integer, primary_key=True, unique=True)
	url = db.Column(db.String(120), unique=True)

	def __init__(self, url):
		self.url = url



@app.route('/', methods=['POST', 'GET'])
def main():
	# ensure the data is stored
	if request.method == 'POST':
		url = request.form['submit_url']
		result = Url.query.filter_by(url=url).first()
		if result:
			flash("nope")
			return redirect(url_for('main'))
		else:
			entry = Url(url)
			db.session.add(entry)
			db.session.commit()
			return redirect(url_for('main'))
	else:
		return render_template('main.html')

@app.route('/<name>/')
def test(name):
	s = "On this page the main infroamtion about the raw data will be shown "
	t = " The raw data is: %s" 
	return s + '\n' + t % name


if __name__ == '__main__':
	db.drop_all()
	db.create_all()
	app.debug = True
	app.run(host='0.0.0.0')