from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import logging, os, lzma, zipfile, tarfile, datetime 
from werkzeug import secure_filename

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

# extract file
# extractable ext: ['.xz','.zip','.rar','.tar','.gz','.tgz']
def extract_file(filename):
	# currently only for 1 level .xz files
	inF = filename
	ext = os.path.splitext(inF)[-1]
	outF = os.path.splitext(inF)[0] #"{}_{}".format(datetime.datetime.now().strftime("%y%m%d%H%M"), os.path.splitext(inF)[0])
	if ext == '.xz':
		with lzma.open(inF, 'rb') as i:
			with open(outF, 'wb') as o:
				o.write(i.read())
	elif ext == '.zip':
		name = os.path.splitext(inF)[0]
		with zipfile.ZipFile(inF, 'r') as z:
			with open(outF, 'wb') as i:
				i.write(z.read(name))
	# couldn't test it
	# elif ext == '.rar':
	# 	with tarfile.open(inF, 'r') as i:
	# 		with open(outF, 'wb') as o:
	# 			o.write(i.read())
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
		file = request.files['upload_log']
		# we trust the user for now
		if file:
			log = LogParser(os.path.splitext(file.filename)[0])
			db.session.add(log)
			db.session.commit()
			# ToDo improve unique names
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