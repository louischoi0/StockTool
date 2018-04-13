import numpy as np
SET_PREPARE_PERIOD = 20

import abc

def get_mean_move(list, perd) :
    res = np.empty(shape=list.shape, dtype=np.float64)
    res[0:perd] = float('nan')

    for i in range(perd, len(list)) :
        res[i] = int(np.average(list[i-perd :i]))
    return res

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
    def csell(self, date,ib):
        pass
    def cbuy(self,date, ib):
        pass
    def gbuyp(self,list , perd,ib=None) :
        pass
    def gbuym(self,ib):
        pass
    def gcellm(self, ib):
        pass
    def gbuys(self,list, perd,ib=None):
        pass
    def gcellp(self,list , perd,ib=None) :
        pass
    def gcells(self,list, perd,ib=None):
        pass
    ###              ###

def watch_cell(date, s,ib) :
    return s.csell(date,ib)
def watch_buy(date, s,ib) :
    return s.cbuy(date,ib)

class ibase() :
    def __init__(self, csv,  name='stock'):
        self.value = csv
        self.name = name

        self.net = [1]
        res = [  (self.value[idx ] / self.value[idx + 1] )  for idx , val in enumerate(self.value[1:]) ]
        self.net = np.append(self.net, res)

        self.N = get_N(self.value)
        self.nM = get_nM(self.value,20)
        self.meanMove5 = get_mean_move(self.value , 5)

        self.bdate = []
        self.sdate = []

        self.bmount = []
        self.smount = []

        self.status = 0
        self.stock = 0
        self.rmount = 0

        self.rnet = np.zeros(self.value.shape[0])
        self.sinfo = np.zeros(self.value.shape[0])
        self.estates = np.zeros(self.value.shape[0])

        self.perd = 20


class sunit() :
    def __init__(self, csv , strat , name='stock') :
        self.ib = ibase(csv, name )
        self.s = strat

    def buy(self, date, value):
        self.ib.status = 1

        tt = self.s.gbuys(self.ib.value, self.ib.perd)
        self.ib.sinfo[date] = tt

        self.ib.rmount -= value * tt
        self.ib.stock += tt

        self.ib.bdate.append(date)
        self.ib.bmount.append(tt*value)

        print("Buy :: " + str(tt) , str(value) , str(date))

    def sell(self, date,value):
        self.ib.status = 0
        tt = self.s.gcells(self.ib.value, self.ib.perd)

        self.ib.rnet[date] = value * tt
        self.ib.sinfo[date] = -tt
        self.ib.rmount += value * tt
        self.ib.stock -= tt

        self.ib.sdate.append(date)
        self.ib.smount.append(tt*value)

        print("Cell :: " + str(tt) , str(value) , str(date))


    def watch(self,date) :
        if self.ib.status :
            return watch_cell(date,self.s,self.ib)
        else :
            return watch_buy(date, self.s,self.ib)

    def act(self, idx, val):
        if self.ib.status :
            self.sell(idx, val)
        else :
            self.buy(idx , val)

    def f(self):
        for idx, v in enumerate(self.ib.value) :
            if self.watch(idx) :
                self.act(idx, v)
            self.info(idx)
            self.ib.estates[idx] = self.eval_estate(idx)

        if self.ib.status :
            self.ib.rmount += self.ib.stock * v

    def rebalance(self, amount) :
        res = self.ib.amount - amount
        self.ib.amount = amount
        self.ib.rmount = res

    def remain_stock(self):
        return self.ib.stock

    def remian_cash(self):
        return self.ib.rmount

    def eval_estate(self,date):
        return int(self.ib.rmount + self.ib.stock * self.ib.value[date])

    def eval_profit(self, date) :
        a = self.ib.sinfo[0:date+1]
        b = self.ib.value[0:date+1]

        a = np.reshape(a,[date+1])
        b = np.reshape (b,[date+1])

        return int(-sum(np.multiply(a,b)) + self.ib.stock * self.ib.value[date][0])

    def info(self, date):
        profit = self.eval_profit(date)
        estate = self.eval_estate(date)
        print('%s :: %s , %s' %(date, profit, estate))

    def supply_cache(self , cache) :
        self.ib.cache = cache
        self.ib.rmount = self.ib.cache