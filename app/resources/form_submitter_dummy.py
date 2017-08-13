import datetime as dt

import numpy as np
import pandas as pd

from flask import render_template
from flask import Response
from flask_restful import Resource
from flask_restful import reqparse
from passlib.hash import pbkdf2_sha256

from resources.utils import pandas_plot_to_html


class FormSubmitterDummy(Resource):
    """Resource class to handle the a post or get request.

    In order to use this class together with an html input form, the
    endpoint where the form makes the request to, and this class should
    be linked via the flask_restful.Api class.

    >>> from flask_restful import Api
    >>> from resources.form_submitter import FormSubmitter
    >>> api = Api(flask_app)
    >>> api.add_resource(FormSubmitter, endpoint)

    Depending on the request method to the endpoint, the corresponding
    method of this class will be executed.

    The input fields defined in the html form are loaded into the class
    instance via the flask_restful.reqparse.RequestParser.

    Arguments to the class can be pased directly to the __init__ (not
    via the parser) by passing then using the `resource_class_kwargs`
    argument

    >>> api.add_resource(FormSubmitter, endpoint,
                         resource_class_kwargs=some_dictionary)
    """

    def __init__(self, select_list_options, data_list_options,
                 radio_buttons_options, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('text_field')
        self.parser.add_argument('number_field', type=int)
        self.parser.add_argument(
            'date_field',
            type=lambda x: dt.datetime.strptime(x, "%Y-%m-%d").date()
        )
        self.parser.add_argument('select_list')
        self.parser.add_argument('data_list')
        self.parser.add_argument('checkbox', default=False,
                                 type=lambda x: True if x == 'on' else False)
        self.parser.add_argument('radio_button')
        self.parser.add_argument('slider', type=int)
        self.parser.add_argument('comment_field')
        self.parser.add_argument('email')
        self.parser.add_argument('password', type=pbkdf2_sha256.hash)
        self.user_inputs = {k: v
                            for k, v in self.parser.parse_args().items()
                            if v is not None}
        self.select_list = select_list_options
        self.data_list = data_list_options
        self.radio_buttons = radio_buttons_options
        super().__init__()

    def get(self):
        res = Response(
            render_template('dummy.html',
                            left_panel='input_dummy.html',
                            tab_0='dataframe.html',
                            tab_1='plot.html',
                            select_list_options=self.select_list,
                            data_list_options=self.data_list,
                            radio_buttons_options=self.radio_buttons)
        )
        return res

    def post(self):
        """Method to execute for a post request.
        """
        inputs = pd.DataFrame(self.user_inputs, index=['value']).T

        df = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
        img = pandas_plot_to_html(df.plot.area(stacked=False).get_figure())

        res = Response(
            render_template("dummy.html",
                            left_panel='input_dummy.html',
                            tab_0='dataframe.html',
                            tab_1='plot.html',
                            select_list_options=self.select_list,
                            data_list_options=self.data_list,
                            radio_buttons_options=self.radio_buttons,
                            dataframe_title="User's input",
                            dataframe=inputs.to_html(),
                            plot_title="Some random plot",
                            plot=img,
                            **self.user_inputs),
            status=200)
        return res
