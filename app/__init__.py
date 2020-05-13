from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)  # 加载配置
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes  # 避免循环引用，所以这一行写在后面
