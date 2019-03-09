#!/usr/bin/env python

## Patrik Vávra
## VAI - 2018

import heapq
from graphVertex import Graph, Vertex
import pygame
import numpy as np


class DStarLite:

	def __init__(self, graph, heur_type, view_range=2):
		self.graph = graph
		self.start = graph.start
		self.goal = graph.goal
		self.range = view_range
		self.k_m = graph.k_m
		self.queue = []
		self.currentVertex = self.start
		self.s_last = self.start
		self.heur_type = heur_type

	def isInQueueDelete(self, s): ## pokud je vrchol v seznamu OPEN, tak vrchol ze seznamu vymaz
		vertices_in_queue = []
		for vertex in self.queue:
			if s in vertex:
				vertices_in_queue.append(vertex)
		if len(vertices_in_queue) >= 2: ## kontrola, jestli neni vrchol v seznamu OPEN vicekrat
			raise ValueError('Více vrcholů ' + vertex + ' ve frontě!') ## pokud ano, vypis chybu
		elif len(vertices_in_queue) > 0:
			self.queue.remove(vertices_in_queue[0])

	def updateVertex(self, u): ## expandovani vrcholu
	    self.isInQueueDelete(u) ## vymaz vrchol ze seznamu OPEN, pokud tam je
	    if (abs(self.graph.Vertices[u].g - self.graph.Vertices[u].rhs) > 1e-5): ## pokud je vrchol nekonzistentni (rhs != g)
	    	heapq.heappush(self.queue, self.calculateKey(u) + (u,)) ## vloz do seznamu OPEN vrchol se spravnou prioritou


	def computeShortestPath(self, isInitialized = True): ## najdi nejkratsi cestu
		if isInitialized == False: ## inicializace seznamu OPEN (staci provest jednou na zacatku)
			heapq.heappush(self.queue, (self.h(self.goal),0)+(self.goal,))
		stop_criterium = 0
		while (self.graph.Vertices[self.currentVertex].rhs != self.graph.Vertices[self.currentVertex].g) or (self.topKey() < self.calculateKey(self.currentVertex)):
			## pocitej dokud neni konzistentni start nebo dokud vrcholy v seznamu OPEN maji nizsi prioritu nez aktualni vrchol
			stop_criterium+=1
			print(stop_criterium)
			if stop_criterium > 200: ## ochrana proti přetečení při rozměrné mapě
				break
#				raise ValueError('V programu došlo k chybě. Spusť znova!')
			k_old = self.topKey() ## nacti starou prioritu vrcholu s nejnizsi prioritou
			if len(self.queue) == 0: ## v pripade prazdneho seznamu OPEN pokracuj
				continue
			u = heapq.heappop(self.queue)[2] ## vyjmi ze seznamu vrchol s nejnizsi prioritou
			k_new = self.calculateKey(u) ## spocitej pro vrchol prioritu, jakou by mel nove mit
			if k_old < k_new:
				heapq.heappush(self.queue, k_new + (u,)) ## vloz do OPEN vrchol s novou prioritou
			elif self.graph.Vertices[u].g > self.graph.Vertices[u].rhs:
				self.graph.Vertices[u].g = self.graph.Vertices[u].rhs ## pokud je vrchol nekonzistentni poloz jeho hodnotu g rovno rhs

				for i in self.graph.Vertices[u].Pred: ## aktualizuj rhs hodnotu predku vrcholu u
					if i != self.goal:
						self.graph.Vertices[i].rhs = min(self.graph.Vertices[i].rhs, self.graph.Vertices[u].g + self.graph.Vertices[i].Succ[u])
					self.updateVertex(i)

			else: ## jinak poloz g hodnotu vrcholu u rovno inf
				g_old = self.graph.Vertices[u].g
				self.graph.Vertices[u].g = float('inf')
				for i in self.graph.Vertices[u].Pred: ## pokud byla hodnota rhs predka vrcholu u vypoctena z hodnoty g vrcholu u, aktualizuj rhs hodnotu predka
					if (self.graph.Vertices[i].rhs == self.graph.Vertices[i].Succ[u] + g_old):
						if i != self.goal:
							minimum = float('inf')
							for succ in self.graph.Vertices[i].Succ:
								min_current = self.graph.Vertices[succ].Succ[i] + self.graph.Vertices[succ].g
								if min_current < minimum:
									minimum = min_current
							self.graph.Vertices[i].rhs = minimum
					self.updateVertex(i)
				if u != self.goal:
					minimum = float('inf') ## aktualizuj hodnotu rhs vrcholu u na zaklade jeho nasledovniku
					for succ in self.graph.Vertices[u].Succ:
						cost = self.graph.Vertices[succ].Succ[u] + self.graph.Vertices[succ].g
						if cost < minimum:
							minimum = cost
					self.graph.Vertices[u].rhs = minimum
				self.updateVertex(u)

	def topKey(self): ## vrat uzel s nejmensi prioritou
		self.queue.sort()
		if len(self.queue) > 0:
			return self.queue[0][:2]
		else:
			return (float('inf'), float('inf')) ## pokud je seznam OPEN prazdny, vrat [inf, inf]

	def calculateKey(self,s): ## vypocti prioritu daneho vrcholu
		return (min(self.graph.Vertices[s].g, self.graph.Vertices[s].rhs) + self.h(s) + self.k_m, min(self.graph.Vertices[s].g, self.graph.Vertices[s].rhs))

	def h(self, s): ## vrat hodnotu dane heuristicke funkce pro cestu z aktualniho do daneho vrcholu
		dx = abs(float(toCoords(self.currentVertex)[0]) - toCoords(s)[0])
		dy = abs(float(toCoords(self.currentVertex)[1]) - toCoords(s)[1])
		if self.heur_type == 1:
			return (dx**2 + dy**2)**0.5  ## euclidovska heuristika
		else:
			return(min(dx,dy)*(2**0.5-1)+max(dx,dy)) ## diagonální heuristika

	def computeNext(self): ## vypocti dalsi vrchol k presunu z aktualniho vrcholu
		min_rhs = float('inf')
		s_next = None
		if self.graph.Vertices[self.currentVertex].rhs == float('inf'):
			raise ValueError('Cesta nebyla nalezena!')
		else:
			for i in self.graph.Vertices[self.currentVertex].Succ: ## vyber dalsiho vrcholu - minimalni hodnota z (hodnota g naslednika + cena prechodu)
				cost = self.graph.Vertices[i].g + self.graph.Vertices[self.currentVertex].Succ[i]
				if cost < min_rhs:
					min_rhs = cost
					s_next = i
			if s_next:
				self.currentVertex = s_next
			else: ## nasledovnik nenalezen
				raise ValueError('Nemůžu najít následovníka k přesunu!')

	def moveScan(self): ## prohledej okolí kvůli zmene prekazek a presun se na dalsi vrchol
		if(self.currentVertex == self.goal):
		    pass
		else:
			s_last = self.currentVertex
			self.getExpandedVertices() ## najdi vsechny expandovane vrcholy kvuli vykresleni
			self.getPathToGoal() ## najdi celou cestu k cili pro vykresleni
			self.computeNext() ## vypocti dalsi vrchol k presunu
			new_coords = toCoords(self.currentVertex)
			if(self.graph.cells[new_coords[1]][new_coords[0]] == -1):  ## nalezena nova prekazka ve vrcholu, kde se chtel robot presunout
				self.currentVertex = s_last  ## robot se nepresunuje, cesta se musi prepocitat
			self.scanObstacles() ## scan okoli


	def scanObstacles(self): ## scan okoli dane parametrem VIEWING_RANGE
		current_pos = toCoords(self.currentVertex)
		cells_update = []
		## Nutno vypocitat, u kterych vrcholu se bude hledat zmena
		for i in range(self.range): ## zavisi na VIEWING_RANGE = self.range
			i+=1
			if current_pos[0] + i < self.graph.x_div:
				for p in range(2*i+1):
				    if current_pos[1]-i+p < self.graph.y_div and current_pos[1]-i+p >= 0:
					    cells_update.append(['x' + str(current_pos[0] + i) + 'y' + str(current_pos[1]-i+p)])
			if current_pos[0] - i >= 0:
				for p in range(2*i+1):
				    if current_pos[1]-i+p < self.graph.y_div and current_pos[1]-i+p >= 0:
					    cells_update.append(['x' + str(current_pos[0] - i) + 'y' + str(current_pos[1]-i+p)])
			if current_pos[1] + i < self.graph.y_div:
				for p in range(2*i-1):
				    if current_pos[0]-i+p+1 < self.graph.x_div and current_pos[0]-i+p+1 >= 0:
					    cells_update.append(['x' + str(current_pos[0] - i+p+1) + 'y' + str(current_pos[1]+i)])
			if current_pos[1] - i >= 0:
				for p in range(2*i-1):
				    if current_pos[0]-i+p+1 < self.graph.x_div and current_pos[0]-i+p+1 >= 0:
					    cells_update.append(['x' + str(current_pos[0] - i+p+1) + 'y' + str(current_pos[1]-i)])

		int_cells_updated = 0
		for coords in cells_update:
			coords_int = toCoords(coords[0])
			if self.graph.cells[coords_int[1],coords_int[0]]  == -1: # detekce nove prekazky
				int_cells_updated +=1
				if int_cells_updated < 2: ## zmena z dane pozice detekovana poprve
					self.k_m += self.h(self.s_last) ## vypocet parametru k_m, ktery se pricita vsem vrcholum v seznamu OPEN - vice v [1]
					self.s_last = self.currentVertex ## nastaveni vrcholu, pro ktery se bude pocitat k_m pri detekci zmeny z jine pozice
				self.graph.cells[coords_int[1],coords_int[0]] = -2 ## nastaveni prekazky jako detekovane
				for pred in self.graph.Vertices[coords[0]].Pred:
					c_old = self.graph.Vertices[pred].Succ[coords[0]]
					self.graph.Vertices[coords[0]].Succ[pred] = float('inf') ## update ceny prechodu
					self.graph.Vertices[pred].Succ[coords[0]] = float('inf') ## update ceny prechodu
					## pokud byla hodnota rhs predchudce vypoctena z vrcholu se zmenenou hodnotou
					if self.graph.Vertices[pred].rhs == (c_old + self.graph.Vertices[coords[0]].g):
						if pred != self.goal:
						    min_rhs = float('inf')
						    for succ in self.graph.Vertices[pred].Succ: ## update hodnoty rhs predchudce na zaklade nasledovniku
						        min_rhs = min(min_rhs, self.graph.Vertices[succ].g + self.graph.Vertices[succ].Succ[pred])
						    self.graph.Vertices[pred].rhs = min_rhs
#
					self.updateVertex(pred)
				self.graph.Vertices[coords[0]].rhs = float('inf')
				self.updateVertex(coords[0])
		if int_cells_updated: ## pokud byl nejaky vrchol zmenen
			self.computeShortestPath() ## najdi novou cestu

	def getExpandedVertices(self): ## najdi vsechny expandovane vrcholy kvuli vykresleni
		row_i = 0
		for row in self.graph.cells:
			column = 0
			for cell in row:
				if cell == 5:
					self.graph.cells[row_i, column] = 0 ## vymaz oznacene vrcholy z predchoziho kroku
				column+=1
			row_i+=1
		for vertex in self.graph.Vertices:
			if self.graph.Vertices[vertex].g != float('inf') and self.graph.Vertices[vertex].g == self.graph.Vertices[vertex].rhs: ## pouze expandovane vrcholy
				coords_int = toCoords(vertex)
				if self.graph.cells[coords_int[1],coords_int[0]] == 0: ## pokud neni vrchol oznacen jako prekazka nebo cesta
					self.graph.cells[coords_int[1],coords_int[0]] = 5 ## oznac jako expandovany vrchol

	def getPathToGoal(self):
		min_rhs = float('inf') ## inicializace
		s_next = self.currentVertex
		row_i = 0
		for row in self.graph.cells:
			column = 0
			for cell in row:
				if cell == 2:
					self.graph.cells[row_i, column] = 0 ## vymaz cestu z predchoziho kroku
				column+=1
			row_i+=1
		while s_next != self.goal: ## dokud nedojdes k cili
			if self.graph.Vertices[s_next].rhs == float('inf'):
				raise ValueError('Cesta nebyla nalezena!')
			min_rhs = float('inf')
			for i in self.graph.Vertices[s_next].Succ: ## hledej dalsi vrchol k presunu na zaklade minimalni hodnoty z (hodnota g naslednika + cena prechodu)
				cost = self.graph.Vertices[i].g + self.graph.Vertices[s_next].Succ[i]
				if cost < min_rhs:
					min_rhs = cost
					s = i

			s_next = s
			if not(s_next):
				raise ValueError('Nemůžu najít následovníka k přesunu!')
			coords_int = toCoords(s_next)
			## pokud je vrchol prazdny nebo oznacen jako expandovany
			if self.graph.cells[coords_int[1],coords_int[0]] == 0 or self.graph.cells[coords_int[1],coords_int[0]] == 5:
				self.graph.cells[coords_int[1],coords_int[0]] = 2 ## vykresli nalezene vrcholy cesty

def toCoords(name): ## ze stringu oznaceni vrcholu vrat x a y-ove hodnoty souradnice vrcholu
        return [int(name.split('x')[1].split('y')[0]), int(name.split('x')[1].split('y')[1])]

def drawGrid(x_div, y_div, Graf, WIDTH, HEIGHT, BORDER, screen): ## vykresli mrizku na zaklade danych parametru
	for row in range(y_div):
	    for column in range(x_div):
	        color = WHITE
	        pygame.draw.rect(screen, colors[Graf.cells[row][column]],
	        [(BORDER + WIDTH) * column + BORDER, (BORDER + HEIGHT) * row + BORDER, WIDTH, HEIGHT]) ## vykresli vrcholy s prislusnou barvou
	        vertex_name = 'x' + str(column) + 'y' + str(row)
	        ## Odkomentuj pro vypisovani hosnot g a rhs vrcholu
#	        basicfont = pygame.font.SysFont('Comic Sans MS', 36)
#	        if(Graf.Vertices[vertex_name].g != float('inf')) and (Graf.Vertices[vertex_name].rhs != float('inf')):
#	            text = basicfont.render(str(round(Graf.Vertices[vertex_name].g))+'+'+str(round(Graf.Vertices[vertex_name].rhs)), True, (0, 0, 200))
#	            textrect = text.get_rect()
#	            textrect.centerx = int(column * (WIDTH + BORDER) + WIDTH / 2) + BORDER
#	            textrect.centery = int(row * (HEIGHT + BORDER) + HEIGHT / 2) + BORDER
#	            screen.blit(text, textrect)

def drawRects(BORDER, WIDTH, HEIGHT, goal_coords, pos_coords, COLOR1, COLOR2, VIEWING_RANGE, screen):
		# Cil vykreslen barvou COLOR1
		pygame.draw.rect(screen, COLOR1, [(BORDER + WIDTH) * goal_coords[0] + BORDER, (BORDER + HEIGHT) * goal_coords[1] + BORDER, WIDTH, HEIGHT])
		# Robot vykreslen jako kruh o barve COLOR
		robot_center = [int(pos_coords[0] * (WIDTH + BORDER) + WIDTH / 2) + BORDER, int(pos_coords[1] * (HEIGHT + BORDER) + HEIGHT / 2) + BORDER]
		pygame.draw.circle(screen, COLOR2, robot_center, int(WIDTH / 3))
		# vykresli oblast viditelnosti kolem robota
		pygame.draw.rect( screen, COLOR2, [robot_center[0] - VIEWING_RANGE * (WIDTH + BORDER)-(WIDTH+BORDER)/2,
		robot_center[1] - VIEWING_RANGE * (HEIGHT + BORDER)-(HEIGHT+BORDER)/2,
	(2*VIEWING_RANGE+1) * (WIDTH + BORDER), (2*VIEWING_RANGE+1) * (HEIGHT + BORDER)], 2)


def generateRandomGrid(x_div, y_div, Graf, start, goal): ## vytvor mrizku o nahodnem umisteni prekazek
	#### POZOR ### vzhledem k nahodnosti nemusi existovat cesta k cili
	Graf.cells = -1*np.random.randint(2, size=(y_div, x_div))
	start_coords = toCoords(start)
	goal_coords = toCoords(goal)
	Graf.cells[start_coords[1],start_coords[0]] = 0 ## zajisti aby v cili a startu nebyly prekazky
	Graf.cells[goal_coords[1],goal_coords[0]] = 0
	######### Odkomentuj pro ulozeni vygenerovane mapy ###########
#	np.savetxt('grid.txt', Graf.cells,fmt='%.0f')

def loadGrid(Graf, GridName, start, goal): ## nacti predem vytvorenou mapu
	Graf.cells = np.loadtxt(GridName, dtype= np.int)
	start_coords = toCoords(start)
	goal_coords = toCoords(goal)
	Graf.cells[start_coords[1],start_coords[0]] = 0 ## zajisti aby v cili a startu nebyly prekazky
	Graf.cells[goal_coords[1],goal_coords[0]] = 0


### Definice potrebnych globalnich promennych ########
# Definice barev
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY1 = (145, 145, 102)
GRAY2 = (77, 77, 51)
BLUE = (0, 0, 80)
YELLOW = (255,255,0)
LIGHT_BLUE = (135,206,235)

# Barvy pouzite pro vykresleni bunek v grafu
colors = {
	0: WHITE,
	1: GREEN,
	2: YELLOW,
	-1: GRAY1,
	-2: GRAY2,
	3: BLUE,
	4: RED,
	5: LIGHT_BLUE
}
