import requests as rq
import numpy as np

import time
import threading

import json
import threading
import sys

INTERVAL_BIT_INFO = 2

class commander() :
	colist = {}
	def __init__(self) :
		pass

	def add_collector(self, key,col) :
		self.colist[key] = col

	def view_epoch(self, key) :
		print(self.colist[key].nlist)

def comd(cmd) :
	while True :
		c = input()
		print("activated")
		
		if c == "ev bit" :
			cmd.view_epoch('bit')
		if c == 'opening' :
			print(cmd.opening)
def get_bit_info_all(*kwars) :
	res = rq.get("https://api.bithumb.com/public/ticker/BTC")
	res = json.loads(res.text)
	return res['data']
def get_bit_info(*kwars) :
	res = get_bit_info_all()
	rnlist = []

	for i in kwars :
		rnlist.append(res[i])	

	return rnlisto

def get_cinfo(code) :
	res = rq.get("https://api.bithumb.com/public/ticker/"+code)
	res = json.loads(res.text)
	return res['data']

def ffilter(res, *kwars) :
	rnlist = []
	for i in kwars :
		rnlist.append(res[i])	

	return rnlist

class rept() :
	tlen = 10
	intv = 2

	def __init__(self,code) :
		self.all = np.empty([self.tlen, 2],dtype=dict)
		self.nlist = np.zeros([self.tlen, 2])
		self.count = 0
		self.inittp = 0
		self.N = np.zeros([self.tlen])
		self.Net = np.zeros([self.tlen])
		self.opening = 0
		self.perd = [10]
		
		self.init()
		self.code = code 
	def init(self) : 
		res = get_bit_info_all()		
		self.nlist[0] = ffilter(res, 'date' , 'min_price')
		self.N[0] = -1
		self.Net[0] = 1

		self.count = 1		
		
		self.opening = ffilter(res, 'opening_price')
		self.closing = ffilter(res,'closing_price')

		threading.Timer( self.intv, self.Task).start()
		print('Task init')
	def Task(self) :
		print(self.count)
		if self.count >= self.tlen :
			print('end call')
			self.endCallback()		
			return
		res = get_cinfo(self.code)
		self.all[self.count] = res
		self.nlist[self.count] = [ res['date'] , res['average_price'] ]
		self.N[self.count] = (self.nlist[self.count - 1][1] - self.nlist[self.count][1]) / self.nlist[self.count-1][1]
		self.Net[self.count] = self.nlist[self.count,1] / self.nlist[self.count -1 ,1]	

		self.After()
		self.count += 1
		threading.Timer( self.intv , self.Task).start() 
	def After(self) :
		if self.count % self.perd[0] == 0:
			self.periodicCondition0()

	def endCallback(self) :
		self.rewrite()
		
	def write(self) :
		dirr = 'data/'
		fname = str(self.nlist[0][0]) +'.csv'
		fname = dirr + fname
		np.savetxt(fname , self.nlist, fmt='%.1f')

	def periodicCondition0(self) :
		perd = self.perd[0]
		pdata = self.Net[self.count - perd:self.count]
		
		res =	np.cumprod(pdata)
		print("pcprod : " + str(res))
		if res[-1] > 1.01 :
			print("intime detected")
				
	def rewrite(self) : 
		self.write()
		self.init()	
	
def engine() :
	bitcol = rept('XRP')
	
	comd = commander()
	comd.add_collector("bit", bitcol)

	return comd
if __name__ == '__main__' :
	c = engine()

	comThread = threading.Thread(target=comd,args=[c])
	comThread.start()
