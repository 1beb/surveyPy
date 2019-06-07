from surveyPy.question import Question
import pandas as pd


def merge(q1,q2):

    if q1.type is not 'categorical':
        raise ValueError('Not categorical')
    if q2.type is not 'categorical':
        raise ValueError('Not categorical')

    res = q1.astype(str) + ' - ' q2.astype(str)
    res = res.astype('category')

    return res

