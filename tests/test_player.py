import pygame
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.entities.player import Player
from src.core.settings import Settings

def test_player():
    """Test básico del jugador"""
    pygame.init()
    settings = Settings()
    
    # Crear jugador
    player = Player(settings, 100, 400)
    
    print("Test Player - PASS")
    print(f"Posición inicial: {player.rect.x}, {player.rect.y}")
    
    # Test de salto
    player.jump()
    print(f"Velocidad Y después de saltar: {player.velocity_y}")
    
    # Actualizar varias veces
    for i in range(20):
        player.update()
    
    print(f"Posición después de 20 updates: {player.rect.x}, {player.rect.y}")
    
    pygame.quit()

if __name__ == "__main__":
    test_player()
