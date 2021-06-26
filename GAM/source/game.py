import pygame, sys
import numpy as np

pygame.init()

icono = pygame.image.load("icon/xo.png")
pygame.display.set_icon(icono)


#Tablero
ANCHO = 600
LARGO = 600
TAB_COL=(0,0,0)
TAB_FILA = 3
TAB_COLUMNA=3
TAMANO = 200

#lineas
LINEA_ANCHO=5
LINEA_COL=(255,245,238)
WIN_LINEA_ANCHO = 10

#circulo
CIR_RAD=60
CIR_ANCHO=10
CIR_COL = (255,0,255)

#Linea
X_ANCHO = 15
X_COLOR= (0,255,255)
ESPACIO=55

pantalla = pygame.display.set_mode((ANCHO, LARGO ))
#Titulo
pygame.display.set_caption('A JUGAR !')
#Color de la pantalla
pantalla.fill(TAB_COL)

# Tablero
tablero = np.zeros((TAB_FILA, TAB_COLUMNA))

#LINEAS DE DIBUJO
def draw_lines():
    #Horizontal
    pygame.draw.line(pantalla, LINEA_COL, (0,200),(600,200), LINEA_ANCHO)
    pygame.draw.line(pantalla, LINEA_COL, (0,400),(600,400), LINEA_ANCHO)
    #Vertical
    pygame.draw.line(pantalla, LINEA_COL, (200,0),(200,600), LINEA_ANCHO)
    pygame.draw.line(pantalla, LINEA_COL, (400,0),(400,600), LINEA_ANCHO)

#Dibujar las figuras
def draw_figures():
    for row in range(TAB_FILA):
        for col in range(TAB_COLUMNA):
            if tablero[row][col]==1:
                pygame.draw.circle( pantalla, CIR_COL, (int( col * 200 + 200/2), int( row * 200 + 200/2)), CIR_RAD, CIR_ANCHO)
            elif tablero[row][col]==2:
                pygame.draw.line( pantalla, X_COLOR, (col * 200 + ESPACIO, row * 200 + 200 - ESPACIO), (col * 200 + 200 - ESPACIO, row * 200 + ESPACIO), X_ANCHO)
                pygame.draw.line( pantalla, X_COLOR, (col * 200 + ESPACIO, row * 200 + ESPACIO), (col * 200 + 200 - ESPACIO, row * 200 + 200 - ESPACIO), X_ANCHO )
def mark_square(row, col, jugador):
    tablero[row][col] = jugador

def available_square(row, col):
    if tablero[row][col]==0:
        return True
    else:
        return False

def is_tablero_full():
    for row in range(TAB_FILA):
        for col in range(TAB_COLUMNA):
            if tablero[row][col]==0:
                return False
    return True

#Verificar ganador
def check_win(jugador):
    #vertical 
    for col in range(TAB_COLUMNA):
        if tablero[0][col]== jugador and tablero[1][col]==jugador and tablero[2][col]==jugador:
            draw_vertical_winning_line(col,jugador)
            return True
    #horizontal 
    for row in range(TAB_FILA):
        if tablero[row][0]==jugador and tablero[row][1]==jugador and tablero[row][2]==jugador:
            draw_horizontal_wining_line(row, jugador)
            return True

    #asc diagonal 
    if tablero[2][0]==jugador and tablero[1][1]==jugador and tablero[0][2]==jugador:
        draw_asc_diagonal(jugador)
        return True

    #desc diagonal
    if tablero[0][0]==jugador and tablero[1][1]==jugador and tablero[2][2]==jugador:
        draw_desc_diagonal(jugador)
        return True

    return False

def draw_vertical_winning_line(col, jugador):
    posX=col*200+100

    if jugador==1:
        color = CIR_COL
    elif jugador ==2:
        color=X_COLOR
    pygame.draw.line(pantalla, color, (posX, 15), (posX, LARGO -15), 15 )

def draw_horizontal_wining_line(row,jugador):
    posY=row*200+100
    if jugador==1:
        color=CIR_COL
    elif jugador==2:
        color=X_COLOR
    pygame.draw.line( pantalla, color, (15, posY), (ANCHO -15, posY), 15)


def draw_asc_diagonal(jugador):
    if jugador==1:
        color=CIR_COL
    elif jugador==2:
        color=X_COLOR
    pygame.draw.line( pantalla, color, (15, LARGO - 15), (ANCHO -15, 15), 15)

def draw_desc_diagonal(jugador):
    if jugador==1:
        color=CIR_COL
    elif jugador==2:
        color=X_COLOR
    pygame.draw.line( pantalla, color, (15, 15),( ANCHO -15, LARGO - 15), 15)

#Reiniciar el juego
def restart():
    pantalla.fill( TAB_COL)
    draw_lines()
    jugador=1
    for row in range(TAB_FILA):
        for col in range(TAB_COLUMNA):
            tablero[row][col]=0

draw_lines()

jugador = 1
game_over = False
#Bucle principal para la pantalla
while True:
    for event in pygame.event.get():
        #Boton salir
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            
            #click en la pantalla
            mouseX=event.pos[0] #x
            mouseY=event.pos[1] #y

            #Imprime click con orden del cuadrado salga el orden de fila y columna (0,0)(0,1)..
            clicked_row=int(mouseY // 200)
            clicked_col=int(mouseX // 200)

            if available_square( clicked_row, clicked_col ):
                if jugador == 1:
                    mark_square( clicked_row, clicked_col, 1 )
                    if check_win(jugador):
                        game_over=True
                    jugador = 2

                elif jugador == 2:
                    mark_square( clicked_row, clicked_col, 2)
                    if check_win(jugador):
                        game_over=True
                    jugador = 1
                draw_figures()
                
        if event.type == pygame.KEYDOWN:
            #Con la letra m se reinicia el juego
            if event.key == pygame.K_m:
                restart()
                jugador=1
                game_over=False
                
    pygame.display.update()