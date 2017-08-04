import json
import logging
import os

from flask import Flask
from flask_gunicorn import run_app
from flask_restful import Api

from resources.form_submitter import FormSubmitter

app = Flask(__name__)


@app.route('/', methods=['POST'])
def profilefit_engine():
    pass


api = Api(app)
api.add_resource(FormSubmitter, '/form-output',
                 resource_class_kwargs={})

if __name__ == '__main__':
    # with gunicorn
    run_app()
    # without gunicorn
    # app.run(host='0.0.0.0', port=5000, debug=True)
