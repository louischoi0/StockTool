import pandas as pd

from sunit import sunit
from strategies import s1

pdd = pd.read_csv('data/list.csv',)

s = sunit(pdd,10000,s1())
s.f()
