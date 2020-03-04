import os, requests
from flask import Flask, request

# db
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "super secret key"

db = SQLAlchemy(app)
from models import Post
migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# -----------------------------------------------------------------------------------------------------
# -------------------------------------- Authentication -----------------------------------------------
# -----------------------------------------------------------------------------------------------------

def auth(header):
    if requests.request("GET", 'http://oauth.infralabs.cs.ui.ac.id/oauth/resource', headers={"Authorization":header}).status_code == 200:
        return True
    else:
        return False

# -----------------------------------------------------------------------------------------------------
# -------------------------------------------- CRUD ---------------------------------------------------
# -----------------------------------------------------------------------------------------------------

@app.route('/post/create/', methods=["POST"])
def post_create():
    if auth(request.headers.get('Authorization')):
        if request.method == 'POST':
            post = Post(title=request.form['title'], content=request.form['content'])
            db.session.add(post)
            db.session.commit()
            return {'message':'success', 'data':post_read(post.id)}
    else:
        return {"message":"Invalid credentials"}

@app.route('/post/read/<id>/')
def post_read(id):
    if auth(request.headers.get('Authorization')):
        post = Post.query.filter_by(id=id).first()
        if post == None:
            return {"message":"Data not found"}
        return {'id': post.id, 'title': post.title, 'content': post.content}
    else:
        return {"message":"Invalid credentials"}

@app.route('/post/update/<id>/', methods=["PATCH"])
def post_upadate(id):
    if auth(request.headers.get('Authorization')):
        if request.method == 'PATCH':
            post = Post.query.filter_by(id=id).first()
            if "title" in request.form:
                post.title = request.form['title']
            if "content" in request.form:
                post.content = request.form['content']
            db.session.commit()
            return {'message':'success', 'data':post_read(post.id)}
    else:
        return {"message":"Invalid credentials"}

@app.route('/post/delete/<id>/', methods=["DELETE"])
def post_delete(id):
    if auth(request.headers.get('Authorization')):
        if request.method == 'DELETE':
            post = Post.query.filter_by(id=id).first()
            db.session.delete(post)
            db.session.commit()
            return {"message":"Deleted!"}
    else:
        return {"message":"Invalid credentials"}