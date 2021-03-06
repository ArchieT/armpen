# -*- coding: utf-8 -*-
from moduly.arm.armpoz import armpoz

from moduly.wartosci.kat import kat
from moduly.wartosci.pos import pos

class rysunek:
	def __init__(self,start):self.start=start

class punkt(rysunek):
	def __init__(self,gdzie): rysunek.__init__(self,gdzie);self.gdzie=gdzie
	def draw(self,ramie,step=0):
		try:
			armpoz(self.gdzie,ramie).przemiesc()
			ramie.opusc_pioro()
			print "NARYSOWANO PUNKT!!!"
		except AssertionError: 
			print "punkt failed"
			#import pdb
			#pdb.post_mortem()
			import traceback
			print traceback.format_exc()

class krzywa(rysunek):
	def __init__(self,start,funkcjadefiniujaca):
		rysunek.__init__(self,start);self.funkcjadefiniujaca=funkcjadefiniujaca
		self.absstopstepprog = self.absolutniestopdlastepprog = 3000
		assert 'czyend' in dir(self)
	def draw(self,ramie,step):
		absstopstepprog = absolutniestopdlastepprog = self.absstopstepprog
		bylprob=False;juzstepprob=0;doprzemend=False
		self.funkcja=funkcja=self.funkcjadefiniujaca(ramie,juzstepprob)
		from moduly.arm.maszyna import nasilnik
		print 'self.start',self.start,'ramie',ramie   #debug
		probstep = self.probstep if self.probstep is not None else step
		try:
			if not bylprob: doprzem = armpoz(self.start,ramie)
			else:
				print juzstepprob
				doprzemfun = funkcja(juzstepprob)
				doprzem = doprzemfun['w']
				print doprzemfun
				doprzemend = doprzemfun['e']
			if not doprzemend:
				doprzem.przemiesc()
				ramie.opusc_pioro()
				ruch = nasilnik(self.funkcja,doprzem,step,str(self))
				ramie.dajnasilnik(ruch)
				print "ZROBILIŚMY KRZYWĄ"
			else: print doprzemend,doprzemfun,doprzem
		except AssertionError:
			bylprob=True
			juzstepprob+=probstep
			doprzemend = self.czyend(juzstepprob)
			print ramie,step,bylprob,juzstepprob,doprzemend    #debug
			#self.draw(ramie,step,bylprob,juzstepprob,doprzemend)
			zrobione = False
			while not doprzemend and not zrobione and juzstepprob<absstopstepprog:
				doprzemend = self.czyend(juzstepprob)
				print "tryin",ramie,step,bylprob,juzstepprob,doprzemend,self
				try:
					doprzemfun = funkcja(juzstepprob)
					doprzemend = doprzemfun['e']
					doprzem = doprzemfun['w']
					if not doprzemend:
						doprzem.przemiesc()
						ramie.opusc_pioro()
						ruch = nasilnik(self.funkcjadefiniujaca(ramie,juzstepprob),doprzem,step,str(self))
						ramie.dajnasilnik(ruch)
						print "ZROBILIŚMY KRZYWĄ"
					zrobione = True
				except AssertionError:
					if not doprzemend and not zrobione:
						juzstepprob+=probstep
						doprzemend = self.czyend(juzstepprob)
			print "Nie zrobiono — limit absstopstepprog" if juzstepprob>=absstopstepprog else "koniec (przynajmniej nie osiągnięto limitu absstopstepprog)"
		print "KONIEC krzywa.draw"
		#except RuntimeError:
		#	print "Mamy RuntimeError, na razie olewamy"

class prosta(krzywa):     #      prosta(cubicbezier):
	def __init__(self,start,end):   #cubicbezier.__init__(self,start,start,end,end)
		ks = start.ka;ke = end.ka; dx=ke['x']-ks['x'] ; dy=ke['y']-ks['y']
		self.czyend = czyend = lambda x: x>=1
		funkdef = lambda arm,probst=0: lambda t: {'w':armpoz({'x':((t+probst)*dx)+ks['x'],'y':((t+probst)*dy)+ks['y']},arm),'e':czyend(t+probst)}
		krzywa.__init__(self,start,funkdef)
		self.probstep = None
		self.end=end

class quadrbezier(krzywa):    # fragment paraboli
	def __init__(self,start,c,end):
		self.c=c;self.end=end;from armpoz import armpoz
		self.czyend = czyend = lambda x: x>=1
		adfunk = lambda u,t: ((1-t)*(1-t)*start.ka[u])+(2*(1-t)*t*c.ka[u])+(t*t*end.ka[u])
		self.probstep = None
		funkdef=lambda arm,probst=0:lambda t:{
			'w':armpoz({
				'x': adfunk('x',t+probst),
				'y': adfunk('y',t+probst)
			},arm),
			'e':czyend(t+probst)
		}
		krzywa.__init__(self,start,funkdef)

class cubicbezier(krzywa):
	def __init__(self,start,c1,c2,end):
		adfunk = lambda u,t: ((1-t)*(1-t)*(1-t)*start.ka[u])+(3*(1-t)*(1-t)*t*c1.ka[u])+(3*(1-t)*t*t*c2.ka[u])+(t*t*t*end.ka[u])
		self.probstep = None
		self.czyend = czyend = lambda x: x>=1
		funkcjadefiniujaca = lambda arm,probst=0: lambda t: {'w':armpoz({
			'x':adfunk('x',t+probst),
			'y':adfunk('y',t+probst)
		},arm),'e':czyend(t+probst)}
		krzywa.__init__(self,start,funkcjadefiniujaca)
		self.c1=c1;self.c2=c2;self.end=end

class plotxy(krzywa):
	def __init__(self,fFromX,zero,oneXzeroY,oneYzeroX): # one will be the maximum — you have to divide the values appropiately
		self.oneXzeroY=oneXzeroY;self.oneYzeroX=oneYzeroX;self.fFromX=fFromX
		self.probstep = None
		#fdef=lambda arm:lambda x:{'w':armpoz({
		#	'x':x,
		#	'y':min(sorted([]))
		#})}
		self.czyend = czyend = lambda x: x>=1
		def fdef(arm,probst=0):
			def tocos(xv):
				x = xv+probst
				kolej = [0,fFromX(x),1];kolej.remove(min(kolej));kolej.remove(max(kolej))
				#tymczasowo będzie jechało po ramce jak wartość poza zakresem, później się to zmieni
				return {'w': armpoz({
					'x':x,
					'y':kolej[0],
				},arm),'e':czyend(x)}
			return tocos
		krzywa.__init__(self,zero,fdef)

class plotrphi(krzywa):
	def __init__(self,fFromPhi,zero,minR,oneR_onZeroPhi,minPhi,maxPhi):  # one is the maximum for radius
		self.probstep = None
		self.fFromPhi=fFromPhi;self.minR=minR;self.oneR_onZeroPhi=oneR_onZeroPhi
		self.minPhi=minPhi;self.maxPhi=maxPhi;self.zero=zero
		vect = zero - pos({'x':0,'y':0})
		onerzerophi_vect = oneR_onZeroPhi - zero
		onerzerophi_vect_PosPol = pos(onerzerophi_vect).po
		rone = onerzerophi_vect_PosPol['r']
		phione = onerzerophi_vect_PosPol['phi']
		self.czyend = czyend = lambda x: x>=maxPhi.deg
		def fdef(arm,probst=0):
			probstk= kat(probst,'deg')
			def tocos(phival):
				phi = kat(phival,'deg')+probstk
				kolej = [0,fFromPhi(phi),1];kolej.remove(min(kolej));kolej.remove(max(kolej))
				#tymczasowo będzie jechało po ramce jak wartość poza zakresem, później się to zmieni
				pwzs = pos({'phi':(phi+phione).naplaszczyznie['katnaplaszczyznie'],'r':kolej[0]*rone})
				# pwzs — pozycja względem zera już przeskalowana
				pjp = pwzs + vect  #pozycja już przesunięta
				return {'w': armpoz(pjp,arm),'e':czyend(phi)}
			return tocos
		krzywa.__init__(self,zero,fdef)

class plotrphiFromZero(krzywa):
	def __init__(self,fFromPhi,minR,oneR_onZeroPhi,minPhi,maxPhi):
		self.fFromPhi=fFromPhi;self.minR=minR;self.oneR_onZeroPhi=oneR_onZeroPhi
		self.probstep = None
		self.minPhi=minPhi;self.maxPhi=maxPhi
		zero = pos({'x':0,'y':0})
		onerzerophi_vect = oneR_onZeroPhi - zero
		onerzerophi_vect_PosPol = pos(onerzerophi_vect).po
		rone = onerzerophi_vect_PosPol['r']
		phione = onerzerophi_vect_PosPol['phi']
		self.czyend = czyend =  lambda x: x>=maxPhi.deg
		def fdef(arm,probst=0):
			probstk = kat(probst,'deg')
			def tocos(phival):
				phi = kat(phival,'deg')+probstk
				kolej = [0,fFromPhi(phi),1];kolej.remove(min(kolej));kolej.remove(max(kolej))
				#tymczasowo będzie jechało po ramce jak wartość poza zakresem, później się to zmieni
				pjp = pos({'phi':(phi+phione).naplaszczyznie['katnaplaszczyznie'],'r':kolej[0]*rone})
				return {'w': armpoz(pjp,arm),'e':czyend(phi)}
			return tocos
		krzywa.__init__(self,zero,fdef)

class arcFromZero(krzywa):
	def __init__(self,r,minPhi,maxPhi):
		#plotrphiFromZero.__init__(self,lambda x:r,r,r,minPhi,maxPhi,kat(0,"deg"))
		self.probstep = 0.0005
		self.r=r;self.minPhi=minPhi;self.maxPhi=maxPhi
		start = pos({'r':r,'phi':minPhi})
		self.czyend = czyend = lambda x: x>=1
		def fdef(arm,probst=0):
			def tocos(xv):
				x = xv+probst
				return {'w': armpoz({'r':r,'phi':minPhi+((maxPhi-minPhi)*x)},arm),'e':czyend(x)}
			return tocos
		krzywa.__init__(self,start,fdef)
#TODO: arcfromelbow
#TODO: allipsefrag
