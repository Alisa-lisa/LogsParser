"""
Celery app and tasks
"""
from application.factories import make_celery, make_flask_app
from application import analyzer
from application import plotting
import os

environment = os.environ.get('ENVIRONMENT')
celery_app = make_celery(make_flask_app("log-parser", environment))


@celery_app.task
def simple_analysis(file):
    """
    Computes simple statistics on the file without parsing it's content
    :param file: path to the file
    :return: tuple containing simple information
    """
    file_size = os.stat(path_name).st_size
    checksum = get_hash(path_name)

    clone = InitialFileUpload.query.filter_by(file_name=path_name, file_size=file_size, checksum=checksum).first()
    if clone:
        print("this file was already uploaded once")
    else:
        upload_time = dt.datetime.now()
        log = InitialFileUpload(path_name, upload_time, file_size, checksum)
        db.session.add(log)
        db.session.commit()

        print("starting ")
        celery_app.parse.delay(path_name)
        print("done celerying")


@celery_app.task(bind=True)
def extract(file_name):
    """
    Decompresses, analyses given the file
    :param file_name: String file name
    :return: None
    """
    analyzer.extract_file(file_name)


@celery_app.task
def parse(path_name):
    """
    Parses the file and displays the geographical distribution
    :param path_name: path to the file
    :return: None
    """
    # return: false_addresses, ipv4_total, ipv6_total, ip_by_country
    data = analyzer.get_statistics(path_name, celery_app.countries)
    plotting.plot(data)