from . import db
from . import login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__='users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))

    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    likes = db.relationship('Like',backref = 'user',lazy = "dynamic")
    dislikes = db.relationship('Dislike',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You Cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'



class Role(db.Model):
    __tablename__ ='roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role', lazy = "dynamic")


    def __repr__(self):
        return f'User {self.name}'





class Pitch(db.Model):
    __tablename__= 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String())
    body = db.Column(db.String())
    category = db.Column(db.String())
    date = db.Column(db.DateTime,default=datetime.utcnow)

    writer = db.Column(db.Integer,db.ForeignKey("users.id"))

    comments = db.relationship('Comment',backref = 'pitch',lazy = "dynamic")
    likes = db.relationship('Like',backref = 'pitch',lazy = "dynamic")
    dislikes = db.relationship('Dislike',backref = 'pitch',lazy = "dynamic")

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_pitch(cls,id):
        pitches = Pitch.query.filter_by(id=id).all()
        return pitches

    @classmethod
    def get_all_pitches(cls):
        pitches = Pitch.query.order_by('-id').all()
        return pitches


    def __repr__(self):
        return f'Pitch {self.pitch_title}'

class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key=True)
    comment_content = db.Column(db.String())
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments

    @classmethod
    def get_all_comments(cls,id):
        comments = Comment.query.order_by('id').all()
        return comments



class Like (db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer,primary_key=True)
    like = db.Column(db.Integer,default=1)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_likes(self):
        db.session.add(self)
        db.session.commit()

    def add_likes(cls,id):
        like_pitch = Like(user = current_user, pitch_id=id)
        like_pitch.save_likes()

    @classmethod
    def get_likes(cls,id):
        like = Like.query.filter_by(pitch_id=id).all()
        return like


    @classmethod
    def get_all_likes(cls,pitch_id):
        likes = Like.query.order_by('-id').all()
        return likes


    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'



class Dislike (db.Model):
    __tablename__ = 'dislikes'

    id = db.Column(db.Integer,primary_key=True)
    dislike = db.Column(db.Integer,default=1)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_dislikes(self):
        db.session.add(self)
        db.session.commit()

    def add_dislikes(cls,id):
        dislike_pitch = Dislike(user = current_user, pitch_id=id)
        dislike_pitch.save_dislikes()

    @classmethod
    def get_dislikes(cls,id):
        dislike = Dislike.query.filter_by(pitch_id=id).all()
        return dislike


    @classmethod
    def get_all_dislikes(cls,pitch_id):
        dislikes = Dislike.query.order_by('-id').all()
        return dislikes


    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'