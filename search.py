from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from numpy import genfromtxt
import pandas as pd

my_data = pd.read_csv('src.csv', delimiter=';', encoding='UTF8')
choices = my_data.loc[:, ['id', 'name']].T


def construct_item(item):
    res = my_data.loc[item[2], :]
    res.at['percent'] = item[1]
    return res


def fuzzy_search(search, similar_threshold=5):
    items = process.extract(search, choices, limit=5)
    threshold = items[0][1] - similar_threshold
    items = [x for x in items if x[1] > threshold]
    return [construct_item(item) for item in items]