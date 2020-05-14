from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)  # 加载配置
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# flask_login在用户访问特定页（view function加了@login_required装饰器）时，如果没有登录，则强制登录，登录后再继续访问原来用户需要访问的页
# 而login_view配置的就是用来login的view function。即它会用url_for去获取对应的url
login.login_view = 'login'


from app import routes  # 避免循环引用，所以这一行写在后面
