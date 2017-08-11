from flask import Flask
from flask import render_template

from flask_restful import Api

from resources.form_submitter import FormSubmitter


app = Flask(__name__)


@app.route('/input-example', methods=['GET'])
def input_example():
    return render_template('input_example.html',
                           select_list=[{'key': 'value_1'},
                                        {'key': 'value_2'},
                                        {'key': 'value_3'}],
                           data_list=[{'country': 'Mexico'},
                                      {'country': 'Netherlands'},
                                      {'country': 'Honduras'}])


# attach a view class to endpoint where the html form makes the request
api = Api(app)
api.add_resource(FormSubmitter, '/output-example',
                 resource_class_kwargs={'extra_0': 'something extra',
                                        'extra_1': 'also extra'})
