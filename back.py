from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import logging
from werkzeug import secure_filename
import os


COMPRESSED_FILES = set(['.xz', '.tar', '.zip'])
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'tex', 'jpg', 'jpeg', 'png', 'log'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
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

# model for the log parser
class LogParser(db.Model):
	__tablename__ = 'log_parser'
	id = db.Column(db.Integer, primary_key=True, unique=True)
	log_name = db.Column(db.String(80), unique=False)
	# think of version representation

	def __init__(self, log_name):
		self.log_name = log_name 

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

# check appropriate extension
def check_extension(filename):
	return '.' in filename and filename.rsplit('.')[-1] in ALLOWED_EXTENSIONS

# function for the logs upload		
@app.route('/logs', methods=['GET', 'POST'])
def upload_log():
	if request.method == 'POST':
		file = request.files['upload_log']
		if file and check_extension(file.filename):
			log = LogParser(file.filename)
			db.session.add(log)
			db.session.commit()
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			return redirect(url_for('upload_log'))
	return render_template('logs_form.html')

@app.route('/logs/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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