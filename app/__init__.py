import os

from rq import Queue
from .worker import conn

from flask import Flask, render_template

q = Queue('high', connection=conn)


def create_app():
    app = Flask(__name__)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=('GET',))
    def index():
        return render_template('index.html')
    return app