from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)#加载配置

from app import routes  # 避免循环引用，所以这一行写在后面
