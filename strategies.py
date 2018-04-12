import sunit
from sunit import sbase
import numpy as np

class s1(sbase) :
    def __init__(self, *args):
        self.n = 0
    def csell_yest(self,ib):
        return True
    def cbuy_yest(self, ib):
        return True
    def gbuyp(self, list, date,ib=None):
        return 1
    def gcellp(self, list, date,ib=None):
        return 1
    def gbuys(self, list, date,ib=None):
        return 1
    def gcells(self,list , date,ib=None):
        return 1


class sbit(sbase) :
	CLRATE = 0.975
	CURATE = 1.1

	OPER = 5
	def csell(self, date, ib):
		if date < self.OPER :
			return False

		anchor = date - 1
		c = np.cumprod(ib.net[anchor:date + 1])[-1]
		if c < self.CLRATE or c > self.CURATE  :
			return True
		else :
			return False

	def cbuy(self, date, ib):
		if date < 5 :
			return False

		anchor = date - self.OPER
		c = np.cumprod(ib.net[anchor:date])[-1]
		print(c)
		if c > 1.08 :
			return True

	def gbuyp(self, list, date,ib=None):
		return 1
	def gcellp(self, list, date,ib=None):
		return 1
	def gbuys(self, list, date,ib=None):
		return 1
	def gcells(self,list , date,ib=None):
		return 1
