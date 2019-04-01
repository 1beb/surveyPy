from surveyPy.question import Question
import pandas as pd


class Survey(question_list):
    def __init__(self, question_list, description=None, start_date=None, end_date=None):
        for item in question_list:
            self._validate(item)

    def _validate(self, item):
        if not isinstance(item, type(Question())):
            raise AttributeError 'Not all survey elements are question objects'
        else:
            pass