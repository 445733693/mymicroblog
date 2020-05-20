from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import os
import logging

app = Flask(__name__)
app.config.from_object(Config)  # 加载配置
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# flask_login在用户访问特定页（view function加了@login_required装饰器）时，如果没有登录，则强制登录，登录后再继续访问原来用户需要访问的页
# 而login_view配置的就是用来login的view function。即它会用url_for去获取对应的url
login.login_view = 'login'

# 将日志打到文件中
if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)  # 每个log文件10k，保留最近10个log文件
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors  # 避免循环引用，所以这一行写在后面
