from flask import Flask

from flask_restful import Api

from resources.form_submitter import FormSubmitter


app = Flask(__name__)

# attach a view class to endpoint where the html form makes the request
api = Api(app)
api.add_resource(
    FormSubmitter, '/',
    resource_class_kwargs={
        'select_list_options': [{'key': 'value_0'},
                                {'key': 'value_1'},
                                {'key': 'value_2'}],
        'data_list_options': [{'country': 'Mexico'},
                              {'country': 'Netherlands'},
                              {'country': 'Honduras'}],
        'radio_buttons_options': ['option_0', 'option_1', 'option_2']})
