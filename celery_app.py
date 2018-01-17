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