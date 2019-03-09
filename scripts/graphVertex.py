#!/usr/bin/env python

## Patrik Vávra
## VAI - 2018

import numpy as np

class Vertex:
    def __init__(self, ID):
    	## V souladu s puvodnim znenim D* lite pouzivam oznaceni pro uzel == vrchol
        self.ID = ID ## klicova hodnota (keyValue) vrcholu
        self.Pred = {} ## mnozina predku vrcholu
        self.Succ = {} ## mnozina nasledovniku vrcholu
        self.g = float('inf') ## odhad hodnoty g vrcholu
        self.rhs = float('inf') ## hodnota rhs vrcholu

    def returnString(self): ## vrat string vrcholu s jeho oznacenim a hodnoty g a rhs
        return 'Vertex: ' + self.ID + ' g: ' + str(self.g) + ' rhs: ' + str(self.rhs)


class Graph:
	def __init__(self, x_div, y_div, edge = 1):
		## Inicializace atributu
		self.Vertices = {}
		self.x_div = x_div
		self.y_div = y_div
		self.edge = edge
		self.cells = np.zeros((y_div, x_div), dtype=np.int)

	def createGraph(self): ## Vytvoreni grafu ze zadanych parametru
		for i in range(self.x_div):
			for j in range(self.y_div):
				vertex = Vertex('x' + str(i) + 'y' + str(j))
				## Vytvoreni mnoziny predku a nasledniku daneho vrcholu
				## 4- smerovy pohyb
				if i > 0: ## vyloucim prave nasledniky a predky, pokud by byli mimo graf
					vertex.Pred['x' + str(i - 1) + 'y' + str(j)] = self.edge
					vertex.Succ['x' + str(i - 1) + 'y' + str(j)] = self.edge
				if i + 1 < self.x_div:  ## leve
					vertex.Pred['x' + str(i + 1) + 'y' + str(j)] = self.edge
					vertex.Succ['x' + str(i + 1) + 'y' + str(j)] = self.edge
				if j > 0: ## horni
					vertex.Pred['x' + str(i) + 'y' + str(j - 1)] = self.edge
					vertex.Succ['x' + str(i) + 'y' + str(j - 1)] = self.edge
				if j + 1 < self.y_div: ## dolni
					vertex.Pred['x' + str(i) + 'y' + str(j + 1)] = self.edge
					vertex.Succ['x' + str(i) + 'y' + str(j + 1)] = self.edge
				## Diagonalni pohyb
				if i > 0 and j > 0:	## vyloucim levy horni roh z nasledovniku a predchudcu
					vertex.Pred['x' + str(i - 1) + 'y' + str(j - 1)] = self.edge*(2**0.5)
					vertex.Succ['x' + str(i - 1) + 'y' + str(j - 1)] = self.edge*(2**0.5)
				if i > 0 and j + 1 < self.y_div:	## levy dolni roh
					vertex.Pred['x' + str(i - 1) + 'y' + str(j + 1)] = self.edge*(2**0.5)
					vertex.Succ['x' + str(i - 1) + 'y' + str(j + 1)] = self.edge*(2**0.5)
				if i + 1 < self.x_div and j + 1 < self.y_div:	## pravy dolni roh
					vertex.Pred['x' + str(i + 1) + 'y' + str(j + 1)] = self.edge*(2**0.5)
					vertex.Succ['x' + str(i + 1) + 'y' + str(j + 1)] = self.edge*(2**0.5)
				if i + 1 < self.x_div and j > 0:	## pravy horni roh
					vertex.Pred['x' + str(i + 1) + 'y' + str(j - 1)] = self.edge*(2**0.5)
					vertex.Succ['x' + str(i + 1) + 'y' + str(j - 1)] = self.edge*(2**0.5)
				self.Vertices['x' + str(i) + 'y' + str(j)] = vertex

	def initialize(self, S_start, S_goal): ## Inicializace grafu
		## Hlidani podminek
		try:
			self.Vertices[S_start]
		except:
			print('Zvolený bod startu není na mapě')
		try:
			self.Vertices[S_goal]
		except:
			print('Zvolený bod cíle není na mapě')
		if S_start == S_goal:
			raise ValueError('Cíl byl zvolen na stejném místě jako start. Vyber jiný bod!')
		self.start = S_start
		self.goal = S_goal
		self.k_m = 0 ## pocatecni hodnota paramtru k_m musi byt nulova
		self.Vertices[self.goal].rhs = 0 ## Nastav rhs cile na 0
