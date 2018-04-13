import pandas as pd
import numpy as np
from sunit import sunit
from strategies import s1
from strategies import sbit
import sys

from univ import universe
from univ import run

pdd0 = pd.read_csv('data/bit-100.csv',)
pdd1 = pd.read_csv('data/bit-100.csv',)
pdd2 = pd.read_csv('data/bit-100.csv',)

pdd0 = np.array(pdd0)
pdd1 = np.array(pdd1)
pdd1 = np.flip(pdd1,axis = 0)

su0 = sunit(pdd0, sbit(),'bit0')
su1 = sunit(pdd1,sbit(),'bit1')

date = len(pdd0)

uv = universe(2, date ,300000)
uv.add_asset1(su0)
uv.add_asset2(su1)

uv.set_weight([0.4, 0.6])
uv.init()

run(uv)

i = 0