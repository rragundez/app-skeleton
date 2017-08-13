from flask import Flask
from flask import render_template

from flask_restful import Api

from dummypackage.dummy_model import train_model
from resources.form_submitter_dummy import FormSubmitterDummy
from resources.form_submitter_iris import FormSubmitterIris

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


# dummy application
api.add_resource(
    FormSubmitterDummy, '/dummy',
    resource_class_kwargs={
        'select_list_options': [{'key': 'value_0'},
                                {'key': 'value_1'},
                                {'key': 'value_2'}],
        'data_list_options': [{'country': 'Mexico'},
                              {'country': 'Netherlands'},
                              {'country': 'Honduras'}],
        'radio_buttons_options': ['option_0', 'option_1', 'option_2']})


# iris flower classifier application
model, confusion, features_imp, features = train_model()


api.add_resource(
    FormSubmitterIris, '/iris-wizard',
    resource_class_kwargs={
        'model': model,
        'features': features,
        'confusion_matrix': confusion,
        'features_imp': features_imp})
