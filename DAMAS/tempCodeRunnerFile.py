
  while True:
    juego.mostrar_tablero()

    if juego.contar_fichas("o") == 0:
      print("¡EL JUGADOR 'x' HA GANADO! 'o' se ha quedado sin fichas.")
      break