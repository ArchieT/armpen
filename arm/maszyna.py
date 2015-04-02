# -*- coding: utf-8 -*-
from __future__ import division
class maszyna:
	def __init__(self):
		from wartosci.kat import kat
		import armpoz
		self.l1 = 20
		self.l2 = 10
		# temporarily givin' up the elbow direction
		# maybe even forever
		#self.maxalphafromzero = kat(180,"deg")
		#self.minalphafromzero = -self.maxalphafromzero
		self.maxbetafromzero = kat(90,"deg")
		self.minbetafromzero = -self.maxbetafromzero
		self.alphaprecision = kat(0.01,"deg")
		self.betaprecision = kat(0.01,"deg")
		self.alphaenginemultiplier = 10
		self.betaenginemultiplier = 20
	def opusc_pioro(self):
		print "Opuszczono pióro"
	def podnies_pioro(self):
		print "Podniesiono pióro"
	def gdziejestesmaszyno(self):
		from armpoz import gdzieramiona;from wartosci.kat import kat
		return gdzieramiona(kat(20,"deg"),kat(40,"deg"),self)  # dummy, to be replaced by real location
	def dajnasilnik(self,co,prec):
		print co
		end = False
		gdzie = 0.0
		done = 0.0
		lastalpha = co.startpoz.alphaodzera
		lastbeta = co.startpoz.beta
		while not end:
			ruchalpha = None
			ruchbeta = None
			syncmultforbetafromalpha = None
			assert gdzie>=done
			if done==gdzie: gdzie+=prec
			elif done<gdzie:
				toc = co.funkcja(gdzie)
				to = toc['w']
				if abs(lastalpha-to.alphaodzera)<self.alphaprecision and abs(lastbeta-to.beta)<self.betaprecision:
					gdzie+=prec
				else:
					if abs(lastalpha-to.alphaodzera)>=self.alphaprecision:
						ruchalpha=to.alphaodzera-lastalpha
					if abs(lastbeta-to.beta)>=self.betaprecision:
						ruchbeta=to.beta-lastbeta
					if ruchalpha is not None and ruchbeta is not None:
						syncmultforbetafromalpha=ruchbeta/ruchalpha
						pass # ruszyć sync
					elif ruchalpha is None and ruchbeta is not None:
						pass # ruszyć alphą
					elif ruchbeta is None and ruchalpha is not None:
						pass # ruszyć betą
				end = toc['e']

class nasilnik:
	def __init__(self,funkcja,startpoz,opis):
		self.funkcja=funkcja;self.startpoz=startpoz
		assert isinstance(opis, str)
		self.__str__ = "Idzie: %s" % opis