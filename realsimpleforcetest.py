# -*- coding: utf-8 -*-
__author__ = 'ArchieT'
from moduly.egzemplarze.real import real
from moduly.wartosci.kat import kat
with real() as arm:
	arm.chamskonasilnik(kat(10,"deg"),kat(10,"deg"))
	arm.chamskonasilnik(kat(20,"deg"),kat(30,"deg"))