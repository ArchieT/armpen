# -*- coding: utf-8 -*-
from __future__ import division
from moduly.arm.maszyna import maszyna
from moduly.wartosci.kat import kat


class fake(maszyna):
	def __init__(self):
		l1 = 26.58
		l2 = l1 * (0.426/0.574)
		# temporarily givin' up the elbow direction
		# maybe even forever
		maxalphafromzero = kat(180,"deg")
		minalphafromzero = -self.maxalphafromzero
		maxbeta = kat(90,"deg")
		minbeta = -maxbeta
		alphaprecision = kat(0.01,"deg")
		betaprecision = kat(0.01,"deg")
		self.drawarea = lambda pozy: True



		maszyna.__init__(self,l1,l2,maxalphafromzero,minalphafromzero,maxbeta,minbeta,alphaprecision,betaprecision)
	def __enter__(self): return self
	def __exit__(self, exc_type, exc_val, exc_tb): pass
	def podnies_pioro(self): print "Podniesiono"
	def opusc_pioro(self): print "Opuszczono"
	def movealpha(self,ruch): print ruch
	def movebeta(self,ruch): print ruch
	def syncedmove(self,a,b): print a,b
