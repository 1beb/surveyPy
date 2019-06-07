import pandas as pd
import numpy as np

# http://pandas.pydata.org/pandas-docs/stable/development/extending.html#extending-subclassing-pandas
# TODO: Adjust below as per above! Use inheritance!

class Survey(pd.DataFrame):
    @property
    def _constructor(self):
        return SubclassedDataFrame

    @property
    def _constructor_sliced(self):
        return SubclassedSeries


class Question(pd.Series):

    @property
    def _constructor(self):
        return Question

    @property
    def _constructor_expanddim(self):
        return Survey

    def __init__(self, obj, question, question_abb=None, responses=None, responses_abb=None, statements=None,
                 statements_abb=None, multipunch=False, base=None, date=False, is_likert=False, flip=False,
                 reorder=True, label_fun=None, separator=None, dnr=None):
        # Data
        self.data = obj.copy()

        # Text Attributes
        self.question = question
        self.question_abb = question_abb
        self.responses = responses
        self.responses_abb = responses_abb
        self.statements = statements
        self.statements_abb = statements_abb

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
        self._recode()

    def _gettype(self):

        if isinstance(self.data, type(pd.DataFrame())):
            if self.responses is not None:
                self.type = 'grouped_categorical'
            else:
                self.type = 'grouped_continuous'
        else:
            if self.responses is not None:
                if len(self.responses) != len(self.data.unique()):
                    raise ValueError('Number of response != unique responses')

                self.type = 'categorical'
            else:
                self.type = 'continuous'

        if self.multipunch is True:
            if len(self.data.shape) != 2:
                raise ValueError('Multipunch question should have more than one column of data')

            self.type = 'multipunch'

        if self.date is True:
            if np.dtype('datetime64[ns]') != self.data.dtypes:
                raise ValueError('Data is date but is not in a datetime format')
            self.type = 'datetime'

    def _recode(self):
        # Categorical
        if self.type == 'categorical':
            if (self.data.dtype == 'int64') or (self.data.dtype == 'float64'):
                self.data = pd.Categorical(self.data.to_list(), categories=range(0, len(self.responses)), ordered=False)
                self.data = self.data.set_categories(self.responses, rename=True)
            else:
                self.data = pd.Categorical(self.data.to_list(), categories=self.responses, ordered=False)

        if self.type == 'grouped_categorical':
            for col in self.data.columns:
                self.data[col] = pd.Categorical(self.data[col].tolist(), categories=self.responses, ordered=False)

        # multipunch
        if self.type == 'multipunch':
            for col in self.data.columns:
                self.data[col] = self.data[col].astype('category')
                self.data[col] = self.data[col].cat.set_categories(['Punch'], rename=True)


    def __str__(self):
        return "%s - (n: %s)" % (self.question, self.data.shape[0])

    def __repr__(self):
        return "<Question Object: %s - (n: %s)>" % (self.question, self.data.shape[0])
