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
	CLRATE = 0.99
	CURATE = 1.01

	OPER = 5

	def csell_yest(self, ib) :
		if ib.count < OPER :
			return false
		
		anchor = ib.count - OPER 
		c = np.cumprod(ib.Net[anchor:ib.count])[-1] 
		if c < CLRATE or c > CURATE  :
			return True
		else :
			return False 
	
	def cbuy_yest(self, ib) :
		if ib.count < 5 :
			return false

		anchor = ib.count - OPER
		c = np.cumprod(ib.Net[anchor:ib.count])[-1]
		print(c)		
		if c > 1.00 :
			return True

	def gbuyp(self, list, date,ib=None):
		return 1
	def gcellp(self, list, date,ib=None):
		return 1
	def gbuys(self, list, date,ib=None):
		return 1
	def gcells(self,list , date,ib=None):
		return 1
