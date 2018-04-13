import numpy as np
from sunit import sunit
def run(universe) :
    universe.a1.f()
    universe.a2.f()


class universe() :
    def __init__(self, nasts, date, inip)  :
        self.asts_ep = np.zeros([nasts,date])
        self.asts_st = np.zeros([nasts,date])
        self.weight = np.zeros([nasts])
        self.sunits = []
        self.initc = np.zeros([nasts])

        self.inip = inip

        self.a1 = None
        self.a2 = None

    def add_asset1(self,ast) :
        self.a1 = ast

    def add_asset2(self, ast):
        self.a2 = ast

    def set_weight(self, weights) :
        self.weight = weights

    def init(self) :
        '''
        self.sunits = np.array(self.initc, dtype = sunit)

        self.initc = np.multiply(self.weight ,self.inip)
        f = np.vectorize(lambda x , y : x.supply_cache(y) , otypes=[sunit])
        f(self.sunits, self.initc)
        '''

        res = np.multiply(self.weight , self.inip)
        self.a1.supply_cache(res[0])
        self.a2.supply_cache(res[1])