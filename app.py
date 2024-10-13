import json
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig" if os.getenv('APP_SETTINGS') == None else os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
@app.route('/')
def hello():
    from models import Result
    from services import acquire_lock, release_lock
    acquire_lock(func=f, lock_name="11", timeout=10)
    release_lock("11")
    return "qwe"


def f():
    time.sleep(10)


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
