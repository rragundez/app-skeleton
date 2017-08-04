import pandas as pd

from flask import render_template
from flask import Response
from flask_restful import Resource
from flask_restful import reqparse


class FormSubmitter(Resource):
    """Resource class to handle the API input form.
    """

    def __init__(self, fitter):
        self.fitter = fitter
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('last_name', default='')
        self.parser.add_argument('date_of_birth')
        self.parser.add_argument('own_risk', type=int)
        self.parser.add_argument('cover_occupants', default=False,
                                 type=lambda x: x == 'on')
        super().__init__()

    def get(self):
        args = dict(self.parser.parse_args())
        df = pd.DaaFrame.from_dict(args)
        res = Response(render_template("dataframe.html",
                                       data=df.to_html(),
                                       title=self.fitter.__class__.__name__),
                       status=200)
        return res
