from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


# 这里的url对应的函数，叫做视图函数view function


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)  # 这里的入参，就是html文件里的变量名


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # flash用于返回给用户提示，其实调用flash的时候，只是Flask保存了一下这个数据，还需要template的渲染
            # 所以需要重定向到一个页面（这里用index)，还需要在那里修改html来显示
            flash('Invalid username or password')
            return redirect(url_for('login'))  # url_for方法可以根据入参视图函数名，得到对应的url，且会自动加url上下文,比写死好
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')  # 获取用户登录前想要访问的url，这个会放在url的next字段里
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')  # 如果没有，或是绝对路径，则重定向到index
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations,you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')  # 取路径变量username
@login_required
def user(username):  # 将路径变量传入view function
    user = User.query.filter_by(username=username).first_or_404()  # 这个会在找不到的时候，自动发送给客户端404错误
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


# 这个装饰器修饰的函数在每个请求分发给具体的view function之前执行
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()  # 之所以不用add，可以直接commit是因为current_user已经是从db加载的user


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
