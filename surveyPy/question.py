import pandas as pd


class Question(object):
    def __init__(self, obj, question, question_abb=None, responses=None, responses_abb=None, statements=None,
                 statements_abb=None, multipunch=False, base=None, date=False, is_likert=False, flip=False,
                 reorder=True, label_fun=None, separator=None, dnr=None):
        # Data
        self._raw = obj.copy()

        # Text Attributes
        self.question = question
        self.question_abb = question_abb if question_abb is not None else []
        self.responses = responses if responses is not None else []
        self.responses_abb = responses_abb if responses_abb is not None else []
        self.statements = statements if statements is not None else []
        self.statements_abb = statements_abb if statements_abb is not None else []

        # Data Attributes
        self.multipunch = multipunch
        self.base = base

        # Logical Attributes
        self.date = date
        self.is_likert = is_likert

        # Plot attributes
        self.flip = flip
        self.reorder = reorder
        self.label_fun = label_fun
        self.separator = separator
        self.dnr = dnr

        # Classify data type
        self._gettype()

    def _gettype(self):

        if isinstance(self._raw, type(pd.DataFrame())):
            if len(self.responses) > 0:
                self.type = 'grouped_categorical'
            else:
                self.type = 'grouped_continuous'
        else:
            if len(self.responses) > 0:
                self.type = 'categorical'
            else:
                self.type = 'continuous'

        if self.multipunch is True:
            self.type = 'multipunch'

        if self.date is True:
            self.type = 'datetime'

    def __str__(self):
        return "%s - (n: %s)" % (self.question, self._raw.shape[0])

    def __repr__(self):
        return "<Question Object: %s - (n: %s)>" % (self.question, self._raw.shape[0])
