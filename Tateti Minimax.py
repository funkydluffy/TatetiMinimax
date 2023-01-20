from math import inf as infinity
from random import choice
import platform
import time
from os import system

"""
Entrenamiento con algoritmo Minimax:
Ta Te Ti resuelto con Minimax en Python.
Gabriel Coria.
"""

HUMANO = -1
IA = +1
tablero = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def analisis(estado):
    """
    Analisis Heuristico de estado:
    De esta manera recibimos el estado actual del
    tablero utilizando dos parametros(estado y jugador)
    y se define si gana un jugador o hay un empate.
    """

    if gana(estado, IA):
        resultado = +1
    elif gana(estado, HUMANO):
        resultado = -1
    else:
        resultado = 0

    return resultado


def gana(estado, jugador):

    """
    Analizamos si un jugador gana(obtiene la "victoria")
    teniendo XXX o OOO ya sea en fila(3 posibilidades),
    columna(3 posibilidades) o diagonal(2 posibilidades),
    utilizando los parametros "estado" y "jugador"
    devolviendo un booleano.
    """

    victoria = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jugador, jugador, jugador] in victoria:
        return True
    else:
        return False


def game_over(estado):

    """
    Analizamos si un jugador gana(terminando el juego)
    utilizando como parametro el tablero actual
    devolviendo un booleano.
    """

    return gana(estado, HUMANO) or gana(estado, IA)


def celdas_vacias(estado):

    """
    Analizamos las celdas vacias para guardarlas en una lista
    utilizando como parametro el estado actual del tablero
    devolviendo una la lista de celdas vacias.
    """

    celdas = []

    for x, fila in enumerate(estado):
        for y, celda in enumerate(fila):
            if celda == 0:
                celdas.append([x, y])

    return celdas


def movida_valida(x, y):

    """
    Validamos una movida solo si la celda está vacía
    usando como parametros los ejes de coordenadas x e y
    devolviendo un booleano.
    """

    if [x, y] in celdas_vacias(tablero):
        return True
    else:
        return False


def set_movida(x, y, jugador):

    """
    La movida impacta en el tablero si la movida es valida
    utilizando los ejes de coordenadas el jugador actual como parametros.
    """

    if movida_valida(x, y):
        tablero[x][y] = jugador
        return True
    else:
        return False


def minimax(estado, depth, jugador):

    """
    La IA elije la mejor movida utilizando como parametros
    el estado actual del tablero, los nódulos del arbol (0 <= depth <= 9)
    y el jugador, dando como resultado una lista con 
    la mejor fila, la mejor columna y el mejor puntaje.
    """
    
    if jugador == IA:
        mejor = [-1, -1, -infinity]
    else:
        mejor = [-1, -1, +infinity]

    if depth == 0 or game_over(estado):
        resultado = analisis(estado)
        return [-1, -1, resultado]

    for celda in celdas_vacias(estado):
        x, y = celda[0], celda[1]
        estado[x][y] = jugador
        resultado = minimax(estado, depth - 1, -jugador)
        estado[x][y] = 0
        resultado[0], resultado[1] = x, y

        if jugador == IA:
            if resultado[2] > mejor[2]:
                mejor = resultado  # max value
        else:
            if resultado[2] < mejor[2]:
                mejor = resultado  # min value

    return mejor


def clean():

    """
    Limpia la consola
    """
    
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(estado, ia_elije, h_elije):
    
    """
    Imprime el tablero en la consola
    utilizando como parametro el estado
    actual del tablero.
    """

    chars = {
        -1: h_elije,
        +1: ia_elije,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for fila in estado:
        for celda in fila:
            symbol = chars[celda]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def turno_ia(ia_elije, h_elije):

    """
    Llama a la función minimax si la depth es menor a 9
    o elije una coordenada al azar
    utilizando como parametros la eleccion del humano
    y de la IA.
    """
    
    depth = len(celdas_vacias(tablero))
    if depth == 0 or game_over(tablero):
        return

    clean()
    print(f'Computer turn [{ia_elije}]')
    render(tablero, ia_elije, h_elije)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        movida = minimax(tablero, depth, IA)
        x, y = movida[0], movida[1]

    set_movida(x, y, IA)
    time.sleep(1)


def turno_humano(ia_elije, h_elije):

    """
    Ejecutamos el turno del humano con una movida válida
    utilizando como parametros la elecciones del humano
    y de la IA.
    """
    
    depth = len(celdas_vacias(tablero))
    if depth == 0 or game_over(tablero):
        return

    # Dictionary of valid moves
    movida = -1
    movidas = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_elije}]')
    render(tablero, ia_elije, h_elije)

    while movida < 1 or movida > 9:
        try:
            movida = int(input('Use numpad (1..9): '))
            coord = movidas[movida]
            can_move = set_movida(coord[0], coord[1], HUMANO)

            if not can_move:
                print('Bad move')
                movida = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    
    """
    Definimos la función principal
    que accederá al resto de las funciones.
    """
    
    clean()
    h_elije = ''  # X or O
    ia_elije = ''  # X or O
    primero = ''  # if human is the first

    # Human chooses X or O to play
    while h_elije != 'O' and h_elije != 'X':
        try:
            print('')
            h_elije = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_elije == 'X':
        ia_elije = 'O'
    else:
        ia_elije = 'X'

    # Human may starts first
    clean()
    while primero != 'Y' and primero != 'N':
        try:
            primero = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(celdas_vacias(tablero)) > 0 and not game_over(tablero):
        if primero == 'N':
            turno_ia(ia_elije, h_elije)
            primero = ''

        turno_humano(ia_elije, h_elije)
        turno_ia(ia_elije, h_elije)

    # Game over message
    if gana(tablero, HUMANO):
        clean()
        print(f'Human turn [{h_elije}]')
        render(tablero, ia_elije, h_elije)
        print('YOU WIN!')
    elif gana(tablero, IA):
        clean()
        print(f'Computer turn [{ia_elije}]')
        render(tablero, ia_elije, h_elije)
        print('YOU LOSE!')
    else:
        clean()
        render(tablero, ia_elije, h_elije)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()