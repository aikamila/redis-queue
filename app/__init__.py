import os

from rq import Queue
from rq.job import Job
from rq.exceptions import NoSuchJobError
from .worker import conn
from .utils import find_3_most_popular

from flask import Flask, render_template, request, redirect, url_for, jsonify

q1 = Queue('high', connection=conn)
q2 = Queue('low', connection=conn)


def create_app():
    app = Flask(__name__)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=('GET',))
    def index():
        url = request.args.get('url', None)
        if url:
            result = q1.enqueue(find_3_most_popular, url, result_ttl=86400)
            return redirect(url_for('process', id=result.id))
        return render_template('index.html')

    @app.route('/processing/<id>', methods=('GET',))
    def process(id):
        return render_template('process.html', id=id)

    @app.route('/check/<id>', methods=('GET',))
    def check(id):
        try:
            if Job.fetch(id=id, connection=conn) and \
                    Job.fetch(id=id, connection=conn).result:
                return jsonify({'ready': True})
            return jsonify({'ready': False, 'error': False})
        except NoSuchJobError:
            return jsonify({'ready': False, 'error': True})

    @app.route('/result/<id>', methods=('GET',))
    def result(id):
        try:
            return render_template('result.html', words=Job.fetch(id=id, connection=conn).result)
        except NoSuchJobError:
            return render_template('job-error.html')


    return app
