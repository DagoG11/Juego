import pygame
import sys
from src.core.game import Game
from src.core.settings import Settings

def main():
    """
    Punto de entrada principal del juego.
    
    Inicializa Pygame, crea la instancia del juego
    y ejecuta el ciclo principal.
    """
    pygame.init() 
    
    settings = Settings()
    game = Game(settings)
    
    try:
        game.run()
    except Exception as e:
        print(f"\n❌ Error crítico: {type(e).__name__}")
        print(f"Mensaje: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
