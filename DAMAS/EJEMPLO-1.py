# ==========================================
# PROYECTO: JUEGO DE DAMAS
# Estructura de Datos
# ==========================================


class Ficha:

  def __init__(self, jugador):
    self.jugador = jugador  # 'o' (claras) o 'x' (oscuras)
    self.es_dama = False  # Cambia a True al llegar al extremo opuesto

  def coronar(self):
    self.es_dama = True

  def __str__(self):
    # Si es Dama se imprime en mayúscula ('O' o 'X')
    return self.jugador.upper() if self.es_dama else self.jugador


class Tablero:

  def __init__(self):
    # FASE 1: Matriz de 8x8 inicializada con None
    self.grid = [[None for _ in range(8)] for _ in range(8)]
    # FASE 2: Posicionamiento inicial de fichas
    self.acomodar_fichas()

    def acomodar_fichas(self):
    for i in range(8):
      for j in range(8):
        if (i + j) % 2 != 0:  # Casillas oscuras del tablero
          if i < 3:
            self.grid[i][j] = Ficha("o")
          elif i > 4:
            self.grid[i][j] = Ficha("x")

  def mostrar_tablero(self):
    print("\n     0     1     2     3     4     5     6     7")
    linea_separadora = "  +" + "-----+" * 8

    for fila in range(8):
      print(linea_separadora)
      contenido_fila = f"{fila} |"
      for col in range(8):
        pieza = self.grid[fila][col]
        if pieza is None:
          contenido_fila += "     |"
        else:
          contenido_fila += f"  {pieza}  |"
      print(contenido_fila)

    print(linea_separadora + "\n")

  # FASE 4: Verificar si el jugador actual tiene capturas obligatorias
  def obtener_capturas_posibles(self, jugador):
    capturas = []
    for f in range(8):
      for c in range(8):
        pieza = self.grid[f][c]
        if pieza is not None and pieza.jugador == jugador:
          # Direcciones de movimiento según tipo de ficha
          direcciones = (
              [(-1, -1), (-1, 1), (1, -1), (1, 1)]
              if pieza.es_dama
              else ([(1, -1), (1, 1)] if jugador == "o" else [(-1, -1), (-1, 1)])
          )

          for df, dc in direcciones:
            f_medio, c_medio = f + df, c + dc
            f_dest, c_dest = f + (2 * df), c + (2 * dc)

            if 0 <= f_dest < 8 and 0 <= c_dest < 8:
              pieza_medio = self.grid[f_medio][c_medio]
              pieza_dest = self.grid[f_dest][c_dest]

              if (
                  pieza_medio is not None
                  and pieza_medio.jugador != jugador
                  and pieza_dest is None
              ):
                capturas.append((f, c, f_dest, c_dest))
    return capturas

  # FASE 3 Y 4: Mover ficha y ejecutar capturas
  def mover(self, f_o, c_o, f_d, c_d, jugador_actual, forzado=None):
    # 1. Validar límites de la matriz
    if not (0 <= f_o < 8 and 0 <= c_o < 8 and 0 <= f_d < 8 and 0 <= c_d < 8):
      print("Error: Las coordenadas deben estar entre 0 y 7.")
      return False, False

    # 0. Si venimos de una captura en cadena, obligar a seguir con la MISMA ficha
    if forzado is not None and (f_o, c_o) != forzado:
      print(
          f"Error: Debes continuar comiendo con la ficha en {forzado},"
          " no con otra."
      )
      return False, False

    pieza = self.grid[f_o][c_o]

    # 2. Validar que la celda origen tenga ficha propia
    if pieza is None or pieza.jugador != jugador_actual:
      print("Error: No hay una ficha tuya en la casilla de origen.")
      return False, False

    # 3. Validar casilla destino vacía
    if self.grid[f_d][c_d] is not None:
      print("Error: La casilla de destino ya está ocupada.")
      return False, False

    diff_f = f_d - f_o
    diff_c = c_d - c_o

    # REGLA: Obligación de comer
    capturas_disponibles = self.obtener_capturas_posibles(jugador_actual)
    # Si venimos de una cadena, la obligación se restringe a esa ficha
    if forzado is not None:
      capturas_disponibles = [
          cap for cap in capturas_disponibles
          if (cap[0], cap[1]) == forzado
      ]
    es_captura = abs(diff_f) == 2 and abs(diff_c) == 2

    if capturas_disponibles and not es_captura:
      print(
          "Error: Estás obligado a comer una ficha rival ya que tienes la"
          " opción."
      )
      return False, False

    # CASO A: Movimiento Simple (1 paso diagonal)
    if abs(diff_f) == 1 and abs(diff_c) == 1:
      if forzado is not None:
        # Ya estábamos en cadena de captura: no se permite un paso simple
        print("Error: Debes seguir comiendo, no puedes hacer un paso simple.")
        return False, False

      if not pieza.es_dama:
        if jugador_actual == "o" and diff_f != 1:
          print("Error: Las fichas normales 'o' solo bajan.")
          return False, False
        if jugador_actual == "x" and diff_f != -1:
          print("Error: Las fichas normales 'x' solo suben.")
          return False, False

      # Ejecutar movimiento simple
      self.grid[f_d][c_d] = pieza
      self.grid[f_o][c_o] = None
      self._evaluar_coronacion(f_d, c_d, pieza)
      return True, False

    # CASO B: Captura de Ficha (2 pasos diagonales)
    elif es_captura:
      f_medio = f_o + (diff_f // 2)
      c_medio = c_o + (diff_c // 2)
      pieza_medio = self.grid[f_medio][c_medio]

      if pieza_medio is None or pieza_medio.jugador == jugador_actual:
        print("Error: No hay una ficha rival para capturar en el trayecto.")
        return False, False

      if not pieza.es_dama:
        if jugador_actual == "o" and diff_f != 2:
          print("Error: Dirección de captura no válida para ficha normal 'o'.")
          return False, False
        if jugador_actual == "x" and diff_f != -2:
          print("Error: Dirección de captura no válida para ficha normal 'x'.")
          return False, False

      # Ejecutar captura
      self.grid[f_d][c_d] = pieza
      self.grid[f_o][c_o] = None
      self.grid[f_medio][c_medio] = None  # Elimina la ficha comida
      self._evaluar_coronacion(f_d, c_d, pieza)

      # Verificar si puede seguir comiendo en cadena CON LA MISMA FICHA
      otra_captura = any(
          cap[0] == f_d and cap[1] == c_d
          for cap in self.obtener_capturas_posibles(jugador_actual)
      )
      return True, otra_captura

    else:
      print("Error: Movimiento no permitido.")
      return False, False

  # FASE 4: Coronación a Dama
  def _evaluar_coronacion(self, fila, col, pieza):
    if not pieza.es_dama:
      if (pieza.jugador == "o" and fila == 7) or (
          pieza.jugador == "x" and fila == 0
      ):
        pieza.coronar()
        print(
            f"¡Felicidades! La ficha '{pieza.jugador}' se ha coronado como"
            " Dama."
        )

  # FASE 5: Evaluar Fin del Juego
  def contar_fichas(self, jugador):
    cant = 0
    for f in range(8):
      for c in range(8):
        if self.grid[f][c] is not None and self.grid[f][c].jugador == jugador:
          cant += 1
    return cant


# ==========================================
# BUCLE PRINCIPAL DE JUEGO
# ==========================================


def jugar():
  juego = Tablero()
  jugador_actual = "o"
  forzado = None  # Casilla (fila, col) de la ficha que debe seguir comiendo

  while True:
    juego.mostrar_tablero()

    # FASE 5: Comprobar condición de victoria por fichas agotadas
    if juego.contar_fichas("o") == 0:
      print("¡EL JUGADOR 'x' HA GANADO! 'o' se ha quedado sin fichas.")
      break
    if juego.contar_fichas("x") == 0:
      print("¡EL JUGADOR 'o' HA GANADO! 'x' se ha quedado sin fichas.")
      break

    print(f"--- TURNO DEL JUGADOR: '{jugador_actual}' ---")

    try:
      if forzado is not None:
        f_o, c_o = forzado
        print(f"Debes continuar comiendo con la ficha en ({f_o}, {c_o}).")
      else:
        f_o = int(input("Fila origen (0-7): "))
        c_o = int(input("Columna origen (0-7): "))
      f_d = int(input("Fila destino (0-7): "))
      c_d = int(input("Columna destino (0-7): "))
    except ValueError:
      print("Error: Ingresa números enteros válidos entre 0 y 7.")
      continue

    exito, puede_repetir = juego.mover(
        f_o, c_o, f_d, c_d, jugador_actual, forzado
    )

    if exito:
      # Si comió una ficha y puede seguir comiendo con la misma pieza,
      # no se cambia el turno y se OBLIGA a continuar con esa ficha
      if puede_repetir:
        forzado = (f_d, c_d)
        print("¡Tienes otro salto disponible! Debes seguir comiendo.")
      else:
        forzado = None
        jugador_actual = "x" if jugador_actual == "o" else "o"


if __name__ == "__main__":
  jugar()