# -*- coding: utf-8 -*-
from moduly.obiekty import rysowania
from moduly.wartosci.pos import pos

class testsource:
	def __init__(self,co): self.co = co
	def __enter__(self): print "start",self.co ; return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		print "bye",self.co
		print "testsource.__exit__",exc_type,exc_val,exc_tb
		import traceback
		#traceback.print_exception(exc_type,exc_val,exc_tb)
	def daj(self):
		#i = 1
		#while i<10:
			#toprostastart = pos({'x':12+i,'y':33.1})
			#print toprostastart
			#toprostaend = pos({'x':13+i,'y':29.7})
			#print toprostaend
			#toprosta = rysowania.prosta(toprostastart, toprostaend)
			#yield toprosta
			#yield rysowania.

			#i+=1
			#print toprosta
		print self.co
			#print i
		for i in range(1,50):
			yield rysowania.punkt(pos({'x':i,'y':i}))
			print i,"done: punkt"
			yield rysowania.punkt(pos({'x':i,'y':i+5}))
			print i,"done:punkt2"
