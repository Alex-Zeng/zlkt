from flask import Flask,render_template,request,session,redirect,url_for,g
import config
from exts import  db
from models import User,Article
from decorators import login_required
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

#登录限制装饰器


@app.route('/')

def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            #session过期期限31天
            session.permanent=True
            return redirect(url_for('index'))
        else:
            return '用户名不存在或密码错误,请确认后再登录'

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.telephone== telephone).first()
        if user:
            return '该手机号码已被注册!'
        elif user.username==username:
            return '该用户名已被使用,请重新输入!'
        elif password1!=password2:
            return '两次输入的密码不相同,请核对后再次提交!'
        else:
            user = User(telephone=telephone,username=username,password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/article/',methods=['GET','POST'])
@login_required
def article():
    if request.method=='GET':
        return render_template('article.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        article = Article(title=title,content=content)
        article.author=user
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
