#!/usr/bin/env python

## Patrik Vávra
## VAI - 2018


###### IMPORT KNIHOVEN A SKRIPTU ##########
from graphVertex import Graph, Vertex
from d_star_lite import *
import pygame
import _thread


######### INICIALIZACE MOZNOSTI PRO VYTVORENI GRAFU ###########

## Pocet bunek (vrcholu) v grafu
x_div = 20
y_div = 20
## Zvol souradnice startu a cile
start = 'x15y2'
goal = 'x2y15'
## Vygeneruj nahodne prekazky
GenerateRandom = False
## Nacti pripravenou mapu
LoadGrid = True
## Vyber heuristiku: 1 = euklidovska; else = diagonalni
heur_type = 2
## Nastav z jake vzdalenosti vidi robot prekazky
VIEWING_RANGE = 3
## Pocet kroku, ktere se provedou pri zmacknuti klavesy f
f_step = 50
## Nastav sirku a vysku jedne bunky v pixelech
WIDTH = 30
HEIGHT = 30
## Nastav sirku mezery mezi bunkami (vrcholy) v pixelech
BORDER = 3


########### DALE NIC NEMENIT ########################
## Vytvor ze zadanych parametru graf
Graf = Graph(x_div, y_div)
Graf.createGraph()
## Inicializace grafu a algotŕitmu D* lite
Graf.initialize(start, goal)
DL = DStarLite(Graf, heur_type, VIEWING_RANGE)
## Pokud zvoleno, nahodne vygeneruj prekazky
if GenerateRandom:
	generateRandomGrid(x_div, y_div, Graf, start, goal)
## Pokud zvoleno, nacti pripravenou mapu
elif LoadGrid:
	## Nastaveni pro nacteni mapy, ktera je v priloze
	x_div = 20
	y_div = 20
	start = 'x0y2'
	goal = 'x15y15'
	Graf.initialize(start, goal)
	DL = DStarLite(Graf, heur_type, VIEWING_RANGE)
	loadGrid(Graf, 'example_grid/grid_20x20_s0_2_g15_15.txt',start, goal)
## Jinak si uzivatel vytvori mapu klikanim

## Inicializace na zaklade zvolenych moznosti
DL.computeShortestPath(False)
goal_coords = toCoords(goal)

########### Inicializace obrazovky Pygame ##############
pygame.init()
## sirka a vyska obrazovky
WINDOW_SIZE = [(WIDTH + BORDER) * x_div + BORDER,
	           (HEIGHT + BORDER) * y_div + BORDER]
screen = pygame.display.set_mode(WINDOW_SIZE)
## jmeno obrazovky
pygame.display.set_caption("D* Lite algoritmus")
## Globalni promenna pro ukonceni smycky
done = False
## Inicializace hodin pro Pygame
clock = pygame.time.Clock()
## Nastav pismo
basicfont = pygame.font.SysFont('Comic Sans MS', 36)

#    # -------- Main Program Loop -----------#

while not done:
	for event in pygame.event.get():  ## Provedeni akce dane uzivatelem
			if event.type == pygame.QUIT:  ## Ukonceni behu programu pri kliknuti na krizek obrazovky
			    done = True
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: ## Zmacknuti mezerniku - posun programu o jeden krok
			    DL.moveScan() ## Pokud je objevena nova prekazka, najde novou trasu, a zustane na miste
			    if DL.currentVertex == goal: ## Pokud je robot v cili, ukonci obrazovku
			        print('Dosel jsem do cile!')
			        done = True

			elif event.type == pygame.MOUSEBUTTONDOWN: ## Pokud uzivatel kliknul do mrizky
			    pos = pygame.mouse.get_pos() ## Nacti pozici bunky, kde uzivatel kliknul
			    column = pos[0] // (WIDTH + BORDER)
			    row = pos[1] // (HEIGHT + BORDER)
			    if(Graf.cells[row][column] == 0 or Graf.cells[row][column] == 2 or Graf.cells[row][column] == 5): ## Bunku nastav jako prekazku
			        Graf.cells[row][column] = -1

			elif event.type == pygame.KEYDOWN and event.key == pygame.K_f: ## Pokud je zmacknuto f, provede se f_step pocet kroku programu
				for i in range(f_step):
#					DL.moveScan()
					try:
						_thread.start_new_thread(DL.moveScan,())
					except:
						print("Nemuzu nastavit multithreading. Zakomentuj od try po print a odkomentuj DL.moveScavn()")
					if DL.currentVertex == goal: ## pokud je dosazeno cile, ukonci rogram
						print('Dosel jsem do cile!')
						done = True
						break
					else:
						## Vykresleni
						screen.fill(BLACK)
						drawGrid(x_div, y_div, Graf, WIDTH, HEIGHT, BORDER,screen)
						drawRects(BORDER, WIDTH, HEIGHT, goal_coords, toCoords(DL.currentVertex), GREEN, RED, VIEWING_RANGE, screen)
						clock.tick(5) ## Omez fps na 5
						pygame.display.flip() ## Vykresli vse na obrazovku
						continue

	## Vykresleni
	screen.fill(BLACK)
	drawGrid(x_div, y_div, Graf, WIDTH, HEIGHT, BORDER,screen)
	drawRects(BORDER, WIDTH, HEIGHT, goal_coords, toCoords(DL.currentVertex), GREEN, RED, VIEWING_RANGE,screen)
	clock.tick(10) ## Omez fps na 10
	pygame.display.flip() ## Vykresli vse na obrazovku
pygame.quit() ## Ukonceni behu programu
