"""
Module containing flask init and several
"""
from flask import request, render_template, redirect, url_for
import hashlib
import os
from application.factories import make_flask_app
# from celery_app import celery_app

environment = os.environ.get('ENVIRONMENT')
app = make_flask_app("log-parser", environment)


def get_hash(file):
    """
    Computes md5 hash for a file to detect duplicates
    :param file: uploaded file
    :return: Hex hash
    """
    s = hashlib.md5()
    with open(file, 'rb') as f:
        for line in f:
            s.update(line)
    return s.hexdigest()


@app.route('/', methods=['POST', 'GET'])
def main():
    """
    Renders the start page, saves given url
    :return: None
    """
    # if request.method == 'POST':
    #     url = request.form['submit_url']
    #     # result = Url.query.filter_by(url=url).first()
    #     if result:
    #         flash("nope")
    #         return redirect(url_for('main'))
    #     else:
    #         entry = Url(url)
    #         db.session.add(entry)
    #         db.session.commit()
    #         return redirect(url_for('main'))
    return render_template('main.html')


@app.route('/logs', methods=['GET', 'POST'])
def upload_log():
    """
    Uploads log file, checks stats, tries to parse and show geo stats
    :return: None
    """
    if request.method == 'POST':
        file = request.files['upload_log']
        if file:
            ext = os.path.splitext(file.filename)[-1]
            if ext in app.config['COMPRESSION_EXTENSIONS']:
                path_name = os.path.join(app.config['UPLOAD_FOLDER'],
                                         file.filename)
                file.save(path_name)
                # celery_app.extract.delay(path_name)
            else:
                path_name = os.path.join(app.config['UPLOAD_FOLDER'],
                                         file.filename)
                file.save(path_name)
        return redirect(url_for('upload_log'))
    return render_template('logs_form.html')


@app.route('/logs/files')
def uploaded_file():
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        print(f)


@app.route('/fin')
def financial_controller():
    return render_template('financial_controller.html')
