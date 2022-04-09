# -*- coding: utf-8 -*-
from tracemalloc import start
import pygame
import numpy as np
from sys import exit
from queue import PriorityQueue

WHIDTH = 800
WIN = pygame.display.set_mode((WHIDTH,WHIDTH))
pygame.display.set_caption("Algoritmo A*")

rojo = (255,0,0)
verde = (0,255,0)
azul  = (0,0,255)
amarillo = (255,255,0)
blanco = (255,255,255)
negro = (0,0,0)
morado = (128,0,128)
naranja = (255,165,0)
gris = (128,128,128)
turquesa = (64,224,208)

class Mapa:
    def __init__ (self,fila,columna,ancho,totalFilas):
        self.fila = fila
        self.columna = columna
        self.x = fila*ancho
        self.y = columna*ancho
        self.color = blanco
        self.vecinos = []
        self.ancho = ancho
        self.totalFilas = totalFilas
    def get_pos (self):
        return self.fila, self.columna
    def es_cerrado (self):
        return self.color == rojo
    def es_abierto (self):
        return self.color == verde
    def es_pared (self):
        return self.color == negro
    def inicio (self):
        return self.color == naranja
    def final (self):
        return self.color == turquesa
    def vacio (self):
        return self.color == blanco
    def poner_inicio (self):
        self.color = naranja
    def poner_final (self):
        self.color = turquesa
    def poner_cerrado (self):
        self.color = rojo
    def poner_abierto (self):
        self.color = verde
    def poner_pared (self):
        self.color = negro
    def ruta (self):
        self.color = morado

    def dibujar  (self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.ancho,self.ancho))
    def actualizarVecinos (self,grid):
        self.vecinos = []
        if self.fila < self.totalFilas-1 and not grid[self.fila+1][self.columna].es_pared():
           self.vecinos.append(grid[self.fila+1][self.columna])
        if self.fila > 0 and not grid[self.fila-1][self.columna].es_pared():
            self.vecinos.append(grid[self.fila-1][self.columna])
        if self.columna < self.totalFilas-1 and not grid[self.fila][self.columna+1].es_pared():
           self.vecinos.append(grid[self.fila][self.columna+1])
        if self.columna > 0 and not grid[self.fila][self.columna-1].es_pared():
            self.vecinos.append(grid[self.fila][self.columna-1])
    def __lt__ (self,otro):
        return False


def h (p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)

def construir_ruta (partida,actual,dibujar):
    while actual in partida:
        actual = partida [actual]
        actual.ruta()
        dibujar()

def algoritmo (dibujar,grid,p_inicio,p_final):
    contador = 0 
    open_set = PriorityQueue()
    open_set.put((0,contador,p_inicio))
    partida = {}
    g_score = {spot:float("inf") for fila in grid for spot in fila}
    g_score [p_inicio] = 0
    f_score = {spot:float("inf") for fila in grid for spot in fila}
    f_score [p_inicio] = h(p_inicio.get_pos(),p_final.get_pos())

    open_set_hash = {p_inicio}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        actual = open_set.get()[2]
        open_set_hash.remove(actual)

        if actual==p_final:
            construir_ruta(partida,p_final,dibujar)
            p_final.poner_final()
            return True
        for vecinos_n in actual.vecinos:
            temp_g_score = g_score[actual]+1
            if temp_g_score < g_score[vecinos_n]:
                partida [vecinos_n] = actual
                g_score[vecinos_n] = temp_g_score
                f_score[vecinos_n] = temp_g_score + h(vecinos_n.get_pos(), p_final.get_pos())
                if vecinos_n not in open_set_hash:
                    contador+=1
                    open_set.put((f_score[vecinos_n],contador,vecinos_n))
                    open_set_hash.add(vecinos_n)
                    vecinos_n.poner_abierto()
        dibujar()

        if actual != p_inicio:
            actual.poner_cerrado()
    return False

def hacer_grid (filas,ancho):
    grid = []
    gap = ancho // filas
    for i in range (filas):
        grid.append([])
        for j in range (filas):
            spot = Mapa (i,j,gap,filas)
            grid[i].append(spot)
    return grid

def dibujar_grid (win,filas,ancho):
    gap = ancho // filas
    for i in range (filas):
        pygame.draw.line(win,gris,(0,i*gap),(ancho,i*gap))
        for j in range (filas):
            pygame.draw.line(win,gris,(j*gap,0),(j*gap,ancho))

def dibujar(win,grid,filas,ancho):
    win.fill(blanco)
    for fila in grid:
        for spot in fila:
            spot.dibujar(win)
    dibujar_grid(win,filas,ancho)
    pygame.display.update()

def get_click_pos (pos,filas,ancho):
    gap=ancho//filas
    y,x=pos
    fila=y//gap
    columna=x//gap
    return fila, columna

def main(win,ancho):
    FILAS=50
    grid=hacer_grid(FILAS,ancho)
    p_inicio = None
    p_final = None
    run = True
    while run:
        dibujar(win,grid,FILAS,ancho)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                fila,columna=get_click_pos(pos,FILAS,ancho)
                spot=grid[fila][columna]
                if not p_inicio and spot != p_final:
                    p_inicio = spot
                    p_inicio.poner_inicio()
                elif not p_final and spot != p_inicio:
                    p_final = spot
                    p_final.poner_final()
                elif spot != p_final and spot != p_inicio:
                    spot.poner_pared()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                fila,columna=get_click_pos(pos,FILAS,ancho)
                spot=grid[fila][columna]
                spot.reset()
                if spot == p_inicio:
                    p_inicio=None
                elif spot == p_final:
                    p_final=None
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and p_inicio and p_final:
                    for fila in grid:
                        for spot in fila:
                            spot.actualizarVecinos(grid)
                    algoritmo(lambda:dibujar(win,grid,FILAS,ancho),grid,p_inicio,p_final)
                if event.key==pygame.K_c:
                    p_inicio=None
                    p_final=None
                    grid=hacer_grid(FILAS,ancho)
    pygame.quit()

main(WIN,WHIDTH)