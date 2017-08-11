import datetime as dt

import pandas as pd

from flask import render_template
from flask import Response
from flask_restful import Resource
from flask_restful import reqparse
from passlib.hash import pbkdf2_sha256


class FormSubmitter(Resource):
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

    def __init__(self, extra_0, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('text_field')
        self.parser.add_argument('number_field', type=int)
        self.parser.add_argument(
            'date_field',
            type=lambda x: dt.datetime.strptime(x, "%Y-%m-%d").date()
        )
        self.parser.add_argument('select_list')
        self.parser.add_argument('data_list')
        self.parser.add_argument('checkbox', default=False)
        self.parser.add_argument('radio_button')
        self.parser.add_argument('slider', type=int)
        self.parser.add_argument('comment_field')
        self.parser.add_argument('email')
        self.parser.add_argument('password', type=pbkdf2_sha256.hash)
        self.kwargs = kwargs

        super().__init__()

    def post(self):
        """Method to execute for a post request.
        """
        args = dict(self.parser.parse_args())
        args.update(self.kwargs)
        df = pd.DataFrame(args, index=['value']).T
        res = Response(render_template("dataframe.html",
                                       data=df.to_html(),
                                       title="Results title"),
                       status=200)
        return res
