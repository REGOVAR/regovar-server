#!env/python3
# coding: utf-8
import os
import sys
import time
import datetime
import logging
import json
import yaml
import subprocess
import tarfile
import shutil

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy import create_engine
# from sqlalchemy_aio import ASYNCIO_STRATEGY

from core.framework import *











def connect(user, password, db, host, port):
    '''Returns a connection and a metadata object'''
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8') #, strategy=ASYNCIO_STRATEGY)
    meta = sqlalchemy.MetaData(bind=con)
    return con, meta


def create_session(engine):
    return scoped_session(sessionmaker(bind=engine))()




async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    app['db'] = engine





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# DATABASE CONNECTION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 




# Connect and map the engine to the database
Base = automap_base()

# TODO / FIXME : why the format with config option doesn't work ...
# db_engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(DATABASE_USER, DATABASE_PWD, DATABASE_HOST,  DATABASE_PORT, DATABASE_NAME))
db_engine = create_engine("postgresql://annso:annso@localhost/annso")

Base.prepare(db_engine, reflect=True)
Base.metadata.create_all(db_engine)
db_session = Session(db_engine)







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MODEL DEFINITION - Build from the database (see sql scripts used to generate the database)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

SampleVariant = Base.classes.sample_variant_hg19
Attribute = Base.classes.attribute
AnnotationDatabase = Base.classes.annotation_database
AnnotationField = Base.classes.annotation_field













# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ANALYSIS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def analysis_from_id(analysis_id):
    """
        Retrieve File with the provided id in the database
    """
    return db_session.query(Analysis).filter_by(id=analysis_id).first();



def analysis_to_json(self, fields=None):
    """
        export the file into json format with only requested fields
    """
    result = {}
    if fields is None:
        fields = Analysis.public_fields
    for f in fields:
        if f == "creation_date" or f == "update_date":
            result.update({f : eval("self." + f + ".ctime()")})
        else:
            result.update({f : eval("self." + f)})
    return result



Analysis               = Base.classes.analysis
Analysis.public_fields = ["id", "name", "template_id", "creation_date", "update_date", "settings"]
Analysis.from_id       = analysis_from_id
Analysis.to_json       = analysis_to_json 











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# TEMPLATE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def template_from_id(template_id):
    """
        Retrieve Template with the provided id in the database
    """
    return db_session.query(Template).filter_by(id=template_id).first();



Template               = Base.classes.template
Template.public_fields = ["id", "name", "author", "description", "version", "creation_date", "update_date"]
Template.from_id       = template_from_id 











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# SAMPLE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def sample_from_id(sample_id):
    """
        Retrieve Sample with the provided id in the database
    """
    return db_session.query(Sample).filter_by(id=sample_id).first();



def sample_to_json(self, fields=None):
    """
        export the sample into json format with only requested fields
    """
    result = {}
    if fields is None:
        fields = Sample.public_fields
    for f in fields:
        result.update({f : eval("self." + f)})
    return result



Sample               = Base.classes.sample
Sample.public_fields = ["id", "name", "comments", "is_mosaic"]
Sample.from_id       = sample_from_id
Sample.to_json       = sample_to_json









# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Variant
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def variant_from_id(reference_id, variant_id):
    """
        Retrieve Sample with the provided id in the database
    """

    return db_session.query(Variant).filter_by(id=variant_id).first();





Variant         = Base.classes.variant_hg19
Variant.from_id = variant_from_id











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# FILE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def file_from_id(file_id):
    """
        Retrieve File with the provided id in the database
    """
    return db_session.query(File).filter_by(id=file_id).first();



def new_file_from_tus(filename, file_size):
    """
        Create a new File object (and entry in the database) with initial data for an upload with TUS protocol
    """

    def get_extension(filename):
        f = os.path.splitext(filename.strip().lower())
        t = f[1][1:]
        if t == "gz":
            return get_extension(f[0]) + f[1]
        return t

    global db_session
    file = File()
    file.filename = filename
    file.type = get_extension(filename)
    file.path = os.path.join(TEMP_DIR, str(uuid.uuid4()))
    file.size = int(file_size)
    file.upload_offset = 0
    file.import_date = datetime.datetime.now()
    db_session.add(file)
    db_session.commit()
    return file



File               = Base.classes.file
File.public_fields = ["id", "filename", "upload_offset", "size", "type", "import_date"]
File.new_from_tus  = new_file_from_tus
File.from_id       = file_from_id










# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# FILTER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def filter_from_id(filter_id):
    """
        Retrieve Filter with the provided id in the database
    """
    return db_session.query(Filter).filter_by(id=filter_id).first();




def filter_to_json(self, fields=None):
    """
        export the filter into json format with only requested fields
    """
    result = {}
    if fields is None:
        fields = Filter.public_fields
    for f in fields:
        result.update({f : eval("self." + f)})
    return result



Filter               = Base.classes.filter
Filter.public_fields = ["id", "analysis_id", "name", "filter", "description"]
Filter.from_id       = filter_from_id
Filter.to_json       = filter_to_json


