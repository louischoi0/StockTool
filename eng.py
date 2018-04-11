import pandas as pd

from sunit import sunit
from strategies import s1
from strategies import sbit
import sys

pdd = pd.read_csv('data/bit-100.csv',)

s = sunit(pdd,10000,s1())
s.f()
