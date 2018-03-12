from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

# 用户表
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone=db.Column(db.String(11),nullable=False)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        self.telephone = kwargs.get('telephone')
        self.username = kwargs.get('username')
        self.password = generate_password_hash(kwargs.get('password')) #加密密码

    def check_password(self,raw_password):
        result =  check_password_hash(self.password,raw_password)
        return result

# 文章表
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DATETIME,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref=db.backref('article'))

# 文章评论表
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    comment_author = db.Column(db.String(10), nullable=False)
    comment_content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now)

    #在评论表可以通过article关联到文章表根据article_id, 同时在文章表也可以通过comment,关联到Comment表
    article = db.relationship('Article', backref=db.backref('comment',order_by=create_time.desc()))