import pygame
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.entities.enemy import Enemy
from src.entities.player import Player
from src.core.settings import Settings

def test_enemy():
    """Test básico del enemigo"""
    pygame.init()
    settings = Settings()
    
    # Crear jugador dummy
    player = Player(settings, 200, 400)
    
    # Crear enemigo
    enemy = Enemy(settings, 0, 400, player)
    
    print("Test Enemy - PASS")
    print(f"Posición inicial del enemigo: {enemy.rect.x}, {enemy.rect.y}")
    
    # Actualizar varias veces
    for i in range(10):
        enemy.update()
    
    print(f"Posición después de 10 updates: {enemy.rect.x}, {enemy.rect.y}")
    
    pygame.quit()

if __name__ == "__main__":
    test_enemy()
