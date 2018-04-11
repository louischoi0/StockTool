import numpy as np
SET_PREPARE_PERIOD = 20

import abc

def get_nM(list, perd) :
    res = np.empty(shape=list.shape, dtype=np.float64)
    res[0:perd] = float('nan')

    for i in range(perd, len(list)) :
        res[i] = int(np.average(get_N(list[i-perd:i])))
    return res

def get_N(list) :
    N = np.array(list[0:-2],dtype=int)

    for i in range( 1, N.shape[0] + 1 ) :
        N[i-1] = int(abs(list[i] - list[i-1]))

    return N

def get_maximum_perd(plist, perd) :
    res = []
    for idx, val in enumerate(plist[0:-perd + 1]) :
        clist = list(plist[idx:idx+perd])
        mval = max(clist)
        nval = plist[idx+ perd - 1]

        if nval >= mval :
            if nval in clist[0:perd-1] :
                lidx = idx + 2

            else :
                lidx = clist.index(nval) + idx
            res.append(lidx)

    res = np.array(list(set(res)),dtype=np.int)
    res.sort()
    return res

def check_sell_all( day0, day1 , smargin ) :
    if day1 / day0 -1 < smargin :
        return True
    else :
        return False

class sbase() :
    ### FOR OVERRIDE ###
    def __init__(self, *args):
        pass
    def csell(self, ib):
        pass
    def cbuy(self,today, ib):
        pass
    def gbuyp(self,list , perd,ib=None) :
        pass
    def gbuys(self,list, perd,ib=None):
        pass
    def gcellp(self,list , perd,ib=None) :
        pass
    def gcells(self,list, perd,ib=None):
        pass
    ###              ###

def watch_cell(date, s,ib) :
    return s.csell(ib)
def watch_buy(date, s,ib) :
    return s.cbuy(ib)

class ibase() :
    nM = None
    N = None
    value = None
    comyest = None
    net = None
    initp = None
    name = None

    def __init__(self, csv, strg , initp,name='stock'):
        self.value = np.array(csv['기준가'])
        self.value.reshape([-1])
        self.comyest = csv['전일대비']
        self.net = np.array(csv['등락율'])
        self.name = name

        self.N = get_N(self.value)
        self.nM = get_nM(self.value,20)

        self.bdate = []
        self.sdate = []

        self.bmount = []
        self.smount = []

        self.status = 0
        self.stock = 0
        self.rmount = initp
        self.stock = 0

        self.perd = 20

class sunit() :
    def __init__(self, csv , initp, strat,name='stock', strg= None) :
        self.ib = ibase(csv, name , initp, strat)
        self.s = strat
    def buy(self, date, value):
        self.ib.status = 1

        tt = self.s.gbuys(self.ib.value, self.ib.perd)

        self.ib.rmount -= value * tt
        self.ib.stock += tt

        self.ib.bdate.append(date)
        self.ib.bmount.append(tt*value)

        print("Buy :: " + str(tt) , str(value) , str(date))

    def sell(self, date,value):
        self.ib.status = 0
        tt = self.s.gcells(self.ib.value, self.ib.perd)

        self.ib.rmount += value * tt
        self.ib.stock -= tt

        self.ib.sdate.append(date)
        self.ib.smount.append(tt*value)

        print("Cell :: " + str(tt) , str(value) , str(date))

    def watch(self,date) :
        if self.ib.status :
            return watch_cell(date,self.ib.value, self.s,self.ib)
        else :
            return watch_buy(date,self.ib.value, self.s,self.ib)

    def act(self, idx, val):
        if self.ib.status :
            self.sell(idx, val)
        else :
            self.buy(idx , val)

    def f(self):
        for idx, v in enumerate(self.ib.value) :
            if self.watch(idx) :
                self.act(idx, v)

        if self.ib.status :
            self.ib.rmount += self.ib.stock * v

        print(self.ib.rmount)

    def rebalance(self, amount) :
        res = self.ib.amount - amount
        self.ib.amount = amount
        self.ib.rmount = res
