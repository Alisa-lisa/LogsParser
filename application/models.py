"""
This module contains DAO objects used in the application
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from application.databases import Base


class Url(Base):
    """
    Url object
    """
    __tablename__ = 'url_counter'

    id = Column(Integer, primary_key=True, unique=True)
    url = Column(String(120), unique=True)

    def __init__(self, url):
        self.url = url


class InitialFileUpload(Base):
    """
    File object with simple characteristics
    """
    __tablename__ = 'initial_upload'

    id = Column(Integer, primary_key=True, unique=True)
    file_name = Column(String(80), unique=False)
    upload_time = Column(DateTime, unique=False)
    file_size = Column(Integer)	# os.stat(filename).st_size
    checksum = Column(String(120)) 	# sha1 or md5 checksum
    parsed = Column(JSONB)

    def __init__(self, file_name, upload_time, file_size, checksum):
        self.file_name = file_name
        self.upload_time = upload_time
        self.file_size = file_size
        self.checksum = checksum
