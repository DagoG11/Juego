import pygame
import random
from src.core.utils import load_image

class Obstacle(pygame.sprite.Sprite):
    """
    Clase para obstáculos del escenario.
    
    Caja 1: Ralentiza 2 segundos (30% velocidad)
    Caja 2: Ralentiza 4 segundos (20% velocidad)
    Caja 3: Detiene completamente
    """
    def __init__(self, settings, x):
        super().__init__()
        self.settings = settings
        
        # Seleccionar caja aleatoria (1, 2 o 3)
        self.box_number = random.randint(1, 3)
        
        # Definir tipo según número (SIN ALEATORIO EN FUNCIONALIDAD)
        self.is_hard = (self.box_number == 3)
        self.is_slowdown_short = (self.box_number == 1)  # 2 segundos
        self.is_slowdown_long = (self.box_number == 2)   # 4 segundos
        
        # Obtener tamaño específico de esta caja desde settings
        self.width, self.height = settings.box_sizes[self.box_number]
        
        # Cargar imagen escalada al tamaño configurado
        self.image = load_image(
            f"assets/images/obstacles/{self.box_number}",
            scale=(self.width, self.height),
            smoothing=settings.sprite_smoothing
        )
        
        # Posicionar más cerca del suelo (VALOR FIJO: 40)
        self.y = settings.ground_level - self.height + 25
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = self.y
        
        # Hitbox de colisión ajustada
        hitbox_margin = int(self.rect.width * 0.075)
        self.hitbox = pygame.Rect(
            self.rect.x + hitbox_margin,
            self.rect.y + hitbox_margin,
            self.rect.width - (hitbox_margin * 2),
            self.rect.height - (hitbox_margin * 2)
        )
        
    def update(self, scroll_speed):
        """
        Actualiza la posición del obstáculo con el scroll del mundo.
        
        Args:
            scroll_speed: Velocidad de desplazamiento horizontal
        """
        self.rect.x -= scroll_speed
        hitbox_margin = int(self.rect.width * 0.075)
        self.hitbox.x = self.rect.x + hitbox_margin
        
    def draw(self, screen):
        """
        Dibuja el obstáculo en pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        screen.blit(self.image, self.rect)
        
        # Sombra proporcional al tamaño de la caja
        shadow_width = int(self.width * 0.9)
        shadow_height = 8
        shadow = pygame.Surface((shadow_width, shadow_height))
        shadow.set_alpha(80)
        shadow.fill((0, 0, 0))
        shadow_x = self.rect.centerx - (shadow_width // 2)
        screen.blit(shadow, (shadow_x, self.settings.ground_level - 2))
