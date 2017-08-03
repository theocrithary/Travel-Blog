#!/usr/bin/env python3

#########################################################
# This is the database processing file. (aka. Models)
# It contains the DB connections, queries and processes
# principles of Models, Views, Controllers (MVC).
#########################################################

# Import modules required for app
import os
import boto
import json
from pymongo import MongoClient
from werkzeug import secure_filename
from config import ecs_test_drive

# Check if running in Pivotal Web Services with MongoDB service bound
if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    MONGOCRED = VCAP_SERVICES["mlab"][0]["credentials"]
    client = MongoClient(MONGOCRED["uri"])
    DB_NAME = str(MONGOCRED["uri"].split("/")[-1])

# Otherwise, assume running locally with local MongoDB instance    
else:
    client = MongoClient('127.0.0.1:27017')
    DB_NAME = "blog"

# Get database connection with database name
db = client[DB_NAME]

# Process submitted form to insert fields into database
def insert_blog(request):
    title = request.form['title']
    category = request.form['category']
    comments = request.form['comments']
    photo_filename = secure_filename(request.files['photo'].filename)
    photo_url = "http://" + ecs_test_drive['ecs_access_key_id'].split('@')[0] + ".public.ecstestdrive.com/" + ecs_test_drive['bucket_name'] + "/" + photo_filename

    db.posts.insert_one({'title':title, 'category':category,'comments':comments, 'photo':photo_url})

def get_blog_posts(category):
    return db.posts.find({"category": category})


def upload_photo(file):
    #### Get ECS credentials from external config file
    ecs_access_key_id = ecs_test_drive['ecs_access_key_id']  
    ecs_secret_key = ecs_test_drive['ecs_secret_key']
    bucket_name = ecs_test_drive['bucket_name']

    ## Open a session with your ECS
    session = boto.connect_s3(ecs_access_key_id, ecs_secret_key, host='object.ecstestdrive.com')  
    ## Get hold of your bucket
    bucket = session.get_bucket(bucket_name)
    filename = secure_filename(file.filename)

    file.save(os.path.join("uploads", filename))
    key = bucket.new_key(filename)
    key.set_contents_from_filename("uploads/" + filename)
    key.set_acl('public-read')
    os.remove("uploads/" + filename)


