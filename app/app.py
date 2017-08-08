from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/input', methods=['GET'])
def input():
    return render_template('input.html',
                           select_list=[{'key': 'value_1'},
                                        {'key': 'value_2'},
                                        {'key': 'value_3'}],
                           data_list=[{'country': 'Mexico'},
                                      {'country': 'Netherlands'},
                                      {'country': 'Honduras'}])
