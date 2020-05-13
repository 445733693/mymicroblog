from flask import render_template, flash, redirect,url_for
from app import app
from app.forms import LoginForm

# 这里的url对应的函数，叫做视图函数view function


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)  # 这里的入参，就是html文件里的变量名


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # flash用于返回给用户提示，其实调用flash的时候，只是Flask保存了一下这个数据，还需要template的渲染
        # 所以需要重定向到一个页面（这里用index)，还需要在那里修改html来显示
        flash('Login request for user {},remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))  # url_for方法可以根据入参视图函数名，得到对应的url，且会自动加url上下文,比写死好
    return render_template('login.html', title='Sign In', form=form)
