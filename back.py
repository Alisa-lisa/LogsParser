from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import logging, os, lzma, zipfile, tarfile
import datetime as dt 
from werkzeug import secure_filename

from analyzer import *

COMPRESSION_EXTENSIONS = set(['.xz', '.tar', '.zip'])


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

# model for the log parser, inintial table for csaving unique files (currently we consider name.size to be primary key)
class LogParser(db.Model):
	__tablename__ = 'initial_upload'
	id = db.Column(db.Integer, primary_key=True, unique=True)
	file_name = db.Column(db.String(80), unique=False) #, primary_key=True
	upload_time = db.Column(db.DateTime, unique=False)

	parse_results = db.relationship('ParseResults', backref='initial_upload', lazy='dynamic')

	def __init__(self, file_name, upload_time):
		self.file_name = file_name 
		self.upload_time = upload_time

# table to store results, with name.timestamp
class ParseResults(db.Model):
	__tablename__ = 'parse_results'
	id = db.Column(db.Integer, db.ForeignKey('initial_upload.id'), primary_key=True)

	file_size = db.Column(db.Integer)	# os.stat(filename).st_size
	unique_code = db.Column(db.Integer) 	# sha1 or md5 checksum
	country = db.Column(db.String(100))	# get from parser
	appearance_number = db.Column(db.Integer)	# get form parser

	def __init__(self, file_size, unique_code, country, appearance_number):
		self.file_size = file_size
		self.unique_code = unique_code
		self.country = country
		self.appearance_number = appearance_number

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

# extract file
# extractable ext: ['.xz','.zip','.rar','.tar','.gz','.tgz']
def extract_file(filename):
	# currently only for 1 level .xz files
	inF = filename
	ext = os.path.splitext(inF)[-1]
	outF = os.path.splitext(inF)[0] #
	if ext == '.xz':
		with lzma.open(inF, 'rb') as i:
			with open(outF, 'wb') as o:
				o.write(i.read())
	elif ext == '.zip':
		name = os.path.splitext(inF)[0]
		with zipfile.ZipFile(inF, 'r') as z:
			with open(outF, 'wb') as i:
				i.write(z.read(name))
	elif ext == '.tar':
		with tarfile.open(inF, mode='r|*') as i:
			i.extractall(path=app.config["UPLOAD_FOLDER"])
	elif ext == '.gz':
		with tarfile.open(inF, mode='r|*') as i:
			i.extractall(path=app.config["UPLOAD_FOLDER"])	


# function for the logs upload		
@app.route('/logs', methods=['GET', 'POST'])
def upload_log():
	if request.method == 'POST':
		# get the file, create FileStorage obj
		file = request.files['upload_log']
		# we trust the user for now
		if file:
			name = os.path.splitext(file.filename)[0]
			time = dt.datetime.now()
			log = LogParser(name, time)
			db.session.add(log)
			db.session.commit()
			if os.path.splitext(file.filename)[-1] in COMPRESSION_EXTENSIONS:
				# save the compressed file. decompress it and delete compressed version
				path_name = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
				file.save(path_name)
				extract_file(path_name) 
				os.remove(path_name)
				return redirect(url_for('upload_log'))
			else:
				path_name = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
				file.save(path_name)
				return redirect(url_for('upload_log'))
	return render_template('logs_form.html')

@app.route('/logs/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/fin')
def financial_controller():
	return render_template('financial_controller.html')

@app.route('/myCv')
def myCV():
	return render_template('myCV.html')

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