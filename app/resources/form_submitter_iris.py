import pandas as pd

from flask import render_template
from flask import Response
from flask_restful import Resource
from flask_restful import reqparse

from dummypackage.dummy_model import get_feature_importances_fig
from resources.utils import pandas_plot_to_html


class FormSubmitterIris(Resource):
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

    def __init__(self, model, features, confusion_matrix, features_imp, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('petal_length_cm', type=float)
        self.parser.add_argument('petal_width_cm', type=float)
        self.parser.add_argument('sepal_length_cm', type=float)
        self.parser.add_argument('sepal_width_cm', type=float)
        self.user_inputs = {k: v
                            for k, v in self.parser.parse_args().items()
                            if v is not None}
        self.model = model
        self.features = features
        self.confusion_matrix = confusion_matrix
        self.features_imp = features_imp
        super().__init__()

    def get(self):
        res = Response(
            render_template('iris.html',
                            left_panel='input_iris.html',
                            tab_0='dataframe.html',
                            tab_1='plot.html',
                            tab_2='dataframe.html')
        )
        return res

    def post(self):
        """Method to execute for a post request.
        """
        fig = get_feature_importances_fig(self.model, self.features_imp)
        img = pandas_plot_to_html(fig)

        prediction, probabilities = self.predict()
        probabilities = probabilities.T
        probabilities.columns = ['Probabilities']

        res = Response(
            render_template("iris.html",
                            left_panel='input_iris.html',
                            tab_0='classification.html',
                            tab_1='plot.html',
                            tab_2='dataframe.html',
                            prediction_label=prediction.title(),
                            probabilities=probabilities.to_html(),
                            plot_title="Features importance with SD",
                            plot=img,
                            dataframe_title='Confusion matrix',
                            dataframe=self.confusion_matrix.to_html(),
                            **self.user_inputs),
            status=200)
        return res

    def predict(self):
        observation = pd.DataFrame(self.user_inputs, index=[0])
        prediction = self.model.predict(observation)
        probabilities = self.model.predict_proba(observation)
        prob = pd.DataFrame(probabilities, columns=self.model.classes_)
        return prediction[0], prob
