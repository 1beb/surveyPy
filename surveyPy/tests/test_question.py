from unittest import TestCase
from surveyPy.question import Question
import pandas as pd


class TestQuestionClass(TestCase):

    df = pd.read_csv('surveyPy/tests/data/sample.csv')

    def test_categorical(self):
        cat = Question(self.df.q2_1, 'This is a categorical question?', responses=['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(cat.type, 'categorical')
        self.assertEqual(cat.question, 'This is a categorical question?')
        self.assertEqual(cat.responses, ['A', 'B', 'C', 'D', 'E'])

    def test_multipunch(self):
        multi = Question(self.df[['q5_1', 'q5_2']], 'This is a multipunch question?', multipunch=True)
        self.assertEqual(multi.type, 'multipunch')
        self.assertTrue(multi._raw.shape[1] > 0)

    def test_multipunch_fail(self):
        # TODO: Should fail if specified multipunch but only one column of data
        pass

    def test_grouped_categorical(self):
        gcat = Question(self.df[['q2_1', 'q2_2']], 'This is a categorical question?',
                        responses=['A', 'B', 'C', 'D', 'E'], statements=['Statement A', 'Statement B'])
        self.assertEqual(gcat.type, 'grouped_categorical')
        self.assertEqual(gcat.question, 'This is a categorical question?')
        self.assertEqual(gcat.responses, ['A', 'B', 'C', 'D', 'E'])

    def test_grouped_continuous(self):
        gcat = Question(self.df[['q2_1', 'q2_2']], 'This is a categorical question?',
                        statements=['Statement A', 'Statement B'])
        self.assertEqual(gcat.type, 'grouped_continuous')
        self.assertEqual(gcat.question, 'This is a categorical question?')
        self.assertEqual(gcat.responses, [])

    def test_date(self):
        dates = pd.date_range(pd.datetime.today(), periods=30, freq='D').to_list()
        dates = pd.Series(dates).sample(1000, replace=True)
        dat = Question(dates, 'This is a date question?', date=True)
        self.assertEqual(dat.type, 'datetime')

    def test_date_fail(self):
        # TODO: Should fail if specified multipunch but only one column of data
        pass

    def test_continuous(self):
        pass