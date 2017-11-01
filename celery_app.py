from application import factories
from application import analyzer
from application import plotting
import pycountry
import os

environment = os.environ.get('ENVIRONMENT')
celery_app = factories.make_celery("log-parser", factories.make_flask_app("log-parser", environment))


@celery_app.task
def extract(args):
	analyzer.extract_file(args)


@celery_app.task
def parse(path_name):
	# return: false_addresses, ipv4_total, ipv6_total, ip_by_country
	data = analyzer.get_statistics(path_name, celery_app.countries)
	plotting.plot(data)