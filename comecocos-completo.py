import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Inicializar pygame
pygame.init()

# Definir constantes
MAPA_ANCHO = 20
MAPA_ALTO = 9
ANCHO, ALTO = 1200, 800
TAMANO_CELDA = min(ANCHO // MAPA_ANCHO, ALTO // MAPA_ALTO)

pantalla = pygame.display.set_mode((MAPA_ANCHO * TAMANO_CELDA, MAPA_ALTO * TAMANO_CELDA))
pygame.display.set_caption("Comecocos")

# Definir colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Definir el mapa del juego (1=pared, 0=camino vacío, 2=punto)
mapa_original = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 2, 2, 1, 1, 2, 1, 1, 0, 0, 1, 1, 2, 1, 1, 2, 2, 2, 1],
    [1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Copiar el mapa original para usar durante el juego
mapa = [fila[:] for fila in mapa_original]

# Definir variables del juego
pac_x, pac_y = 1, 1
fan_x, fan_y = 10, 5
puntos = 0
velocidad = 100
total_puntos = sum(fila.count(2) for fila in mapa_original)  # Contar el total de puntos en el mapa

# Función para reiniciar el juego
def reiniciar_juego():
    """Restablece el estado del juego a sus valores iniciales."""
    global pac_x, pac_y, fan_x, fan_y, puntos, mapa
    # Reiniciar la posición del jugador a la coordenada inicial
    pac_x, pac_y = 1, 1
    # Reiniciar la posición del fantasma
    fan_x, fan_y = 10, 5
    # Restablecer el puntaje a cero
    puntos = 0
    # Volver a cargar el mapa con sus elementos originales
    mapa = [fila[:] for fila in mapa_original]

# Función para mover el personaje principal
def mover_pacman(dx, dy):
    """Mueve el Pac-Man en la dirección dada y actualiza la recolección de puntos."""
    global pac_x, pac_y, puntos
    # Verificar que el movimiento no atraviese paredes
    nueva_x = pac_x + dx
    nueva_y = pac_y + dy
    
    # Verificar que la nueva posición esté dentro de los límites del mapa
    if 0 <= nueva_x < MAPA_ANCHO and 0 <= nueva_y < MAPA_ALTO:
        # Verificar que no sea una pared (valor 1)
        if mapa[nueva_y][nueva_x] != 1:
            # Si hay un punto en la nueva posición, incrementar el puntaje
            if mapa[nueva_y][nueva_x] == 2:
                puntos += 1
            
            # Actualizar la posición del jugador en el mapa
            mapa[nueva_y][nueva_x] = 0  # Eliminar el punto si lo había
            pac_x, pac_y = nueva_x, nueva_y
            
            return True  # Movimiento exitoso
    
    return False  # Movimiento inválido

# Función para mover el fantasma
def mover_fantasma():
    """Mueve el fantasma de forma aleatoria en direcciones permitidas."""
    global fan_x, fan_y
    
    # Seleccionar una dirección aleatoria entre arriba, abajo, izquierda o derecha
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(direcciones)
    
    for dx, dy in direcciones:
        nueva_x = fan_x + dx
        nueva_y = fan_y + dy
        
        # Comprobar que el movimiento no atraviese paredes y esté dentro de los límites
        if 0 <= nueva_x < MAPA_ANCHO and 0 <= nueva_y < MAPA_ALTO and mapa[nueva_y][nueva_x] != 1:
            # Actualizar la posición del fantasma en el mapa
            fan_x, fan_y = nueva_x, nueva_y
            return True
    
    return False  # No se pudo mover

# Función para dibujar el mapa y los personajes
def dibujar_juego():
    """Dibuja el mapa del juego, el Pac-Man, el fantasma y la puntuación."""
    pantalla.fill(NEGRO)
    
    # Dibujar el mapa
    for y in range(MAPA_ALTO):
        for x in range(MAPA_ANCHO):
            rect = pygame.Rect(x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            
            if mapa[y][x] == 1:  # Pared
                pygame.draw.rect(pantalla, AZUL, rect)
            elif mapa[y][x] == 2:  # Punto
                pygame.draw.circle(pantalla, BLANCO, 
                                  (x * TAMANO_CELDA + TAMANO_CELDA // 2, 
                                   y * TAMANO_CELDA + TAMANO_CELDA // 2), 
                                  TAMANO_CELDA // 8)
    
    # Dibujar el Pac-Man
    pygame.draw.circle(pantalla, AMARILLO, 
                      (pac_x * TAMANO_CELDA + TAMANO_CELDA // 2, 
                       pac_y * TAMANO_CELDA + TAMANO_CELDA // 2), 
                      TAMANO_CELDA // 2 - 2)
    
    # Dibujar el fantasma
    pygame.draw.circle(pantalla, ROJO, 
                      (fan_x * TAMANO_CELDA + TAMANO_CELDA // 2, 
                       fan_y * TAMANO_CELDA + TAMANO_CELDA // 2), 
                      TAMANO_CELDA // 2 - 2)
    
    # Mostrar puntuación
    fuente = pygame.font.SysFont('Arial', 24)
    texto = fuente.render(f'Puntos: {puntos}/{total_puntos}', True, BLANCO)
    pantalla.blit(texto, (10, 10))
    
    pygame.display.flip()

# Función para verificar si el juego ha terminado
def verificar_fin_juego():
    """Verifica si el juego ha terminado ya sea por victoria o por derrota."""
    # Verificar si el jugador ha sido capturado por el fantasma
    if pac_x == fan_x and pac_y == fan_y:
        mostrar_game_over("¡Has sido capturado!")
        return True
    
    # Verificar si el jugador ha recogido todos los puntos
    if puntos >= total_puntos:
        mostrar_game_over("¡Has ganado!")
        return True
    
    return False

# Función para mostrar la pantalla de Game Over
def mostrar_game_over(mensaje):
    """Muestra la pantalla de Game Over y pregunta si el jugador quiere reiniciar."""
    # Dibujar el mensaje de Game Over en la pantalla
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont('Arial', 36)
    texto_game_over = fuente.render('GAME OVER', True, ROJO)
    texto_mensaje = fuente.render(mensaje, True, BLANCO)
    
    pantalla.blit(texto_game_over, (MAPA_ANCHO * TAMANO_CELDA // 2 - texto_game_over.get_width() // 2, 
                                    MAPA_ALTO * TAMANO_CELDA // 2 - 50))
    pantalla.blit(texto_mensaje, (MAPA_ANCHO * TAMANO_CELDA // 2 - texto_mensaje.get_width() // 2, 
                                  MAPA_ALTO * TAMANO_CELDA // 2))
    
    pygame.display.flip()
    
    # Esperar un tiempo antes de preguntar
    pygame.time.wait(2000)
    
    # Preguntar al usuario si desea reiniciar
    preguntar_volver_a_jugar(mensaje)

# Función para preguntar si el jugador quiere volver a jugar
def preguntar_volver_a_jugar(mensaje):
    """Muestra un cuadro de diálogo preguntando si el jugador quiere volver a jugar."""
    # Crear una ventana emergente con tkinter para mostrar un mensaje de juego terminado
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    
    # Preguntar al usuario si desea jugar nuevamente con opciones "Sí" o "No"
    respuesta = messagebox.askyesno("Juego Terminado", f"{mensaje}\n¿Quieres jugar de nuevo?")
    
    if respuesta:
        # Si el usuario elige "Sí", reiniciar el juego
        reiniciar_juego()
    else:
        # Si el usuario elige "No", cerrar pygame y terminar el programa
        pygame.quit()
        sys.exit()

# Función principal del juego
def main():
    reloj = pygame.time.Clock()
    tiempo_ultima_actualizacion = pygame.time.get_ticks()
    tiempo_movimiento_fantasma = pygame.time.get_ticks()
    
    ejecutando = True
    while ejecutando:
        tiempo_actual = pygame.time.get_ticks()
        
        # Capturar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        
        # Controlar movimiento del Pac-Man
        teclas = pygame.key.get_pressed()
        if tiempo_actual - tiempo_ultima_actualizacion > velocidad:
            movimiento_realizado = False
            
            if teclas[pygame.K_UP]:
                movimiento_realizado = mover_pacman(0, -1)
            elif teclas[pygame.K_DOWN]:
                movimiento_realizado = mover_pacman(0, 1)
            elif teclas[pygame.K_LEFT]:
                movimiento_realizado = mover_pacman(-1, 0)
            elif teclas[pygame.K_RIGHT]:
                movimiento_realizado = mover_pacman(1, 0)
            
            if movimiento_realizado:
                tiempo_ultima_actualizacion = tiempo_actual
        
        # Mover el fantasma cada cierto tiempo
        if tiempo_actual - tiempo_movimiento_fantasma > velocidad * 1.5:
            mover_fantasma()
            tiempo_movimiento_fantasma = tiempo_actual
        
        # Dibujar el juego
        dibujar_juego()
        
        # Verificar si el juego ha terminado
        if verificar_fin_juego():
            tiempo_ultima_actualizacion = tiempo_actual
        
        reloj.tick(60)  # Limitar a 60 FPS
    
    pygame.quit()
    sys.exit()

# Iniciar el juego si este script se ejecuta directamente
if __name__ == "__main__":
    main()
