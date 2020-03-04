from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Post {}>'.format(self.title) 