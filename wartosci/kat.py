# -*- coding: utf-8 -*-
from __future__ import division
class kat:
	degOLrad = lambda w: lambda x,a: x if a==w else (math.degrees(x) if w=="deg" else math.radians(x) if w=="rad" else None) if a==("deg" if w=="rad" else "rad" if w=="deg" else None) else None
	def __init__(self,w,a):
		self.w=w;self.a=a;self.degval=None;self.radval=None;self.sinval=None;self.cosval=None;self.tanval=None
		assert a in ("rad","deg")
	@property
	def deg(self):
		if self.w==0: return 0
		if self.degval is None: self.degval=self.degOLrad("deg")(self.w,self.a)
		return self.degval
	@property
	def rad(self):
		if self.w==0: return 0
		if self.radval is None: self.radval=self.degOLrad("rad")(self.w,self.a)
		return self.radval
	def skalar(self,czynnik):
		if self.w==0: return self
		return kat(w*czynnik,a)
	def dodajinny(self,inny,wczymifnotsame):
		return kat(inny.w+self.w,self.a) if inny.a==self.a else kat(inny.eval(wczymifnotsame)+eval('self.'+wczymifnotsame),wczymifnotsame)
	@property
	def ujemny(self): return kat(-self.w,self.a)
	@property
	def naplaszczyznie(self):
		zdiva=divmod(self.w,kat(360,"deg").eval(self.a))
		return {'katnaplaszczyznie': kat(zdiva[1],self.a),'pelnych':int(zdiva[0])}
	@property
	def cwiartka(self):
		zdiva=divmod(self.w,kat(90,"deg").eval(self.a))
		return {'cwiartka':int(zdiva[0]),'ostry':kat(zdiva[1],self.a)}
	def porownaj(self,inny):
		return (self.deg==inny.deg or self.rad==inny.rad)
	@property
	def sin(self):
		if sinval is not None: return self.sinval
		from math import sin
		self.sinval = sin(self.rad)
		return self.sinval
	@property
	def cos(self):
		if cosval is not None: return self.cosval
		from math import cos
		self.cosval = cos(self.rad)
		return self.cosval
	@property
	def tan(self):
		if tanval is not None: return self.tanval
		from math import tan
		self.tanval = tan(self.rad)
		return self.tanval
class arctrig(kat):
	def __init__(self,val,trigt):
		assert trigt in ['cos','sin','tan']
		from math import sqrt
		if trigt=='cos': from math import acos as atrig
		elif trigt=='sin': from math import asin as atrig
		elif trigt=='tan': from math import atan as atrig
		kat.__init__(self,atrig(val),'rad')
		if trigt=='cos': self.cosval = val ; self.sinval=sqrt(1-(val**2)) ; self.tanval=sqrt(1-(val**2))/val
		elif trigt=='sin': self.sinval = val ; self.cosval=sqrt(1-(val**2)) ; self.tanval=val/sqrt(1-(val**2))
		elif trigt=='tan': self.tanval = val ; self.sinval=val/sqrt(1+(val**2)) ; self.cosval=1/sqrt(1+(val**2))