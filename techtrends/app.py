import sqlite3
import logging
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

db_con_count = 0


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    #app.logger.info("DB accessed")
    global db_con_count 
    db_con_count += 1
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.error(f"Article with ID {post_id} doesn't exist")
        return render_template('404.html'), 404
    else:
        app.logger.info(f"Article with the title: '{post['title']}' retrieved")
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info(f"About Us page retrieved.")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f"New article with the title '{title}' created")
            return redirect(url_for('index'))

    return render_template('create.html')

# Healthz endpoint
@app.route("/healthz")
def healthz():
    try:
        response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
        )
        app.logger.info("Healthz request successfull")
    
    except Exception as e:
        response = app.response_class(
            response=json.dumps({"result": "not OK - unhealthy"}),
            status=500,
            mimetype='application/json'
        )
    return response

# Metrics endpoint
@app.route('/metrics')
def metrics():
    con = get_db_connection()
    cur = con.cursor()
    post_count = cur.execute("SELECT COUNT(id) FROM posts").fetchone()[0]
    con.close()

    # doesnt work anymore when logs are streamed -> use global variable
    # everytime get_db_connection is called "DB accessed" gets logged
    # db_con_count = open("app.log").read().count("DB accessed")

    response = app.response_class(
        response=json.dumps({"db_connection_count": db_con_count, "post_count": post_count}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info("Metrics request successfull")
    return response

# start the application on port 5000
if __name__ == "__main__":
    #logging.basicConfig(filename='app.log',level=logging.DEBUG)
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:%(asctime)s, %(message)s')
    app.run(host='0.0.0.0', port='3111')
   
