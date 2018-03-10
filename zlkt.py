from flask import Flask, render_template, request, session, redirect, url_for, g
import config
from exts import db
from sqlalchemy.sql import or_
from models import User, Article,Comment
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 登录限制装饰器


@app.route('/')
def index():
    articles = Article.query.order_by('-create_time').all()
    return render_template('index.html', articles=articles)

@app.route('/detail/<id>/')
def detail(id):
    article = Article.query.filter(Article.id==id).first()

    return render_template('detail.html',article=article)

@app.route('/add_comment/<article_id>',methods=['POST'])
def add_comment(article_id):
    comment_content = request.form.get('comment_content')
    comment_author = request.form.get('comment_author')
    comment= Comment(comment_content=comment_content,comment_author=comment_author,article_id=article_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail',id=article_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    articles = Article.query.filter(or_(Article.title.contains(q),Article.content.contains(q))).order_by('-create_time')
    return render_template('index.html', articles=articles)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user  :
            if User.check_password(user,raw_password=password):
                session['user_id'] = user.id
                session['username'] = user.username
                # session过期期限31天
                session.permanent = True
                return redirect(url_for('index'))
            else:
                return '密码错误,请重新输入'
        else:
            return '用户名不存,请确认后再登录'


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # telephone = request.form.get('telephone')
        telephone = '15220094541'  # 不开放注册,暂时只能自己用
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if User.query.filter(User.telephone == telephone).first():
            return '该手机号码已被注册!'
        elif User.query.filter(User.username == username).first():
            return '该用户名已被注册!'
        elif password1 != password2:
            return '两次输入的密码不相同,请核对后再次提交!'
        else:
            user1 = User(telephone=telephone, username=username, password=password1)
            db.session.add(user1)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/article/', methods=['GET', 'POST'])
@login_required
def article():
    if request.method == 'GET':
        return render_template('article.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        article = Article(title=title, content=content)
        article.author = user
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
