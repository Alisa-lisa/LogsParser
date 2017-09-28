from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import hashlib, os
import datetime as dt 

# from application.log_parser import analyzer

from main_app import app


def get_hash(file):
	s = hashlib.md5()
	with open(file, 'rb') as f:
		for line in f:
			s.update(line)
	return s.hexdigest()


# app.config['UPLOAD_FOLDER']
# app.config['SQLALCHEMY_DATABASE_URI']

# db = SQLAlchemy(app)
#
# class Url(db.Model):
# 	__tablename__ = 'url_counter'
# 	id = db.Column(db.Integer, primary_key=True, unique=True)
# 	url = db.Column(db.String(120), unique=True)
#
# 	def __init__(self, url):
# 		self.url = url
#
# class InitialFileUpload(db.Model):
# 	__tablename__ = 'initial_upload'
# 	id = db.Column(db.Integer, primary_key=True, unique=True)
# 	file_name = db.Column(db.String(80), unique=False)
# 	upload_time = db.Column(db.DateTime, unique=False)
# 	file_size = db.Column(db.Integer)	# os.stat(filename).st_size
# 	checksum = db.Column(db.String(120)) 	# sha1 or md5 checksum
# 	parse_results = db.relationship('ParseResult', backref='initial_upload', lazy='joined')
#
# 	def __init__(self, file_name, upload_time, file_size, checksum):
# 		self.file_name = file_name
# 		self.upload_time = upload_time
# 		self.file_size = file_size
# 		self.checksum = checksum
#
# class ParseResult(db.Model):
# 	__tablename__ = 'parse_results'
# 	id = db.Column(db.Integer, db.ForeignKey('initial_upload.id'), primary_key=True)
# 	country = db.Column(db.String(100))
# 	appearance_number = db.Column(db.Integer)
#
# 	def __init__(self, country, appearance_number):
# 		self.country = country
# 		self.appearance_number = appearance_number

"""  upper part should be   """

@app.route('/', methods=['POST', 'GET'])
def main():
	# if request.method == 'POST':
	# 	url = request.form['submit_url']
	# 	print(url)
	# 	# result = Url.query.filter_by(url=url).first()
	# 	# if result:
	# 	# 	flash("nope")
	# 	# 	return redirect(url_for('main'))
	# 	# else:
	# 	# 	# entry = Url(url)
	# 	# 	# db.session.add(entry)
	# 	# 	# db.session.commit()
	# 	# 	return redirect(url_for('main'))
	# else:
	return render_template('main.html')


# # function for the logs upload
# @app.route('/logs', methods=['GET', 'POST'])
# def upload_log():
# 	if request.method == 'POST':
# 		# get the file, create FileStorage obj
# 		file = request.files['upload_log']
# 		path_name = ''
# 		extracted = ''
# 		# we trust the user for now
# 		print("extracting")
# 		if file:
# 			# check whetrher file is compressed, save decompressed version of the uploaded file
# 			if os.path.splitext(file.filename)[-1] in COMPRESSION_EXTENSIONS:
# 				# save the compressed file. decompress it and delete compressed version
# 				path_name = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
# 				file.save(path_name)
# 				analyzer.extract_file.spool({"filename":path_name})
# 				extracted = os.path.splitext(path_name)[0]
# 			else:
# 				path_name = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
# 				file.save(path_name)
# 			# count file size in bytes
# 			print(extracted)
# 			file_size = os.stat(path_name).st_size
# 			# count checksum
# 			checksum = get_hash(path_name)
# 			# find, whether such (file_name, size, checksum) was already uploaded
# 			clone = InitialFileUpload.query.filter_by(file_name=path_name, file_size=file_size, checksum=checksum).first()
# 			# # this file was already uploaded
# 			if clone:
# 				print("this file was already uploaded once")
# 			else:
# 				upload_time = dt.datetime.now()
# 				log = InitialFileUpload(path_name, upload_time, file_size, checksum)
# 				db.session.add(log)
# 				db.session.commit()
#
# 			# 	# run the parser here
# 			# 	print("spooling")
# 			# 	false_addresses, ipv4_total, ipv6_total, ip_by_country = analyzer.get_statistics.spool(path_name)
# 			# 	print("done spooling")
#
#
# 			return redirect(url_for('upload_log'))
# 	return render_template('logs_form.html')
#
# @app.route('/logs/<filename>')
# def uploaded_file(filename):
# 	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#
# @app.route('/fin')
# def financial_controller():
# 	return render_template('financial_controller.html')
#
# @app.route('/<name>/')
# def test(name):
# 	s = "On this page the main infroamtion about the raw data will be shown "
# 	t = " The raw data is: %s"
# 	return s + '\n' + t % name
#
