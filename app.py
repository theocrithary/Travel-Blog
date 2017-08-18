#!/usr/bin/env python3

##################################################
# This is the main application file.
# It has been kept to a minimum using the design
# principles of Models, Views, Controllers (MVC).
##################################################

# Import modules required for app
import os
from flask import Flask, render_template, request
from models import insert_blog, get_blog_posts, upload_photo

# Create a Flask instance
app = Flask(__name__)

##### Define routes #####
@app.route('/')
def home():
    return render_template('home.html',url="home")

# This route accepts GET and POST calls
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
    	upload_photo(request.files['photo'])			# Call function in 'models.py' to upload photo to ECS
    	insert_blog(request)							# Call function in 'models.py' to process the database transaction
    	return render_template('submitpost.html')
    else:
        return render_template('newpost.html')

@app.route('/travel')
def travel():
    travel_posts = get_blog_posts("travel")				# Call function in 'models.py' to process the database transaction
    return render_template('travel.html',blog_posts=travel_posts,url='travel')

@app.route('/calista')
def calista():
	calista_posts = get_blog_posts("calista")			# Call function in 'models.py' to process the database transaction
	return render_template('calista.html',blog_posts=calista_posts,url='calista')

@app.route('/events')
def events():
    events_posts = get_blog_posts("events")				# Call function in 'models.py' to process the database transaction
    return render_template('events.html',blog_posts=events_posts,url='events')

@app.route('/photo/<path:photo>')
def photo(photo):
    return render_template('photo.html',photo=photo)

##### Run the Flask instance, browse to http://<< Host IP or URL >>:5000 #####
if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '5000')), threaded=True)