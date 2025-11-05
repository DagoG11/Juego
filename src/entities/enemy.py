import pygame
from src.core.utils import load_animation_frames

class Enemy(pygame.sprite.Sprite):
    """Clase del enemigo perseguidor."""
    def __init__(self, settings, x, y, player):
        super().__init__()
        self.settings = settings
        self.player = player
        
        print("\n=== CARGANDO SPRITES DEL PERRO ===")
        
        self.running_frames = load_animation_frames(
            "assets/images/dog", 9, settings.enemy_size, start_index=1, smoothing=settings.sprite_smoothing
        )
        
        # Animación
        self.current_frame = 0
        self.animation_speed = 0.22
        self.image = self.running_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        
        # ALTURA INICIAL DEL PERRO - MÁS CERCA DEL SUELO
        # Cambia este valor: más bajo = más cerca del suelo
        self.rect.bottom = self.settings.ground_level + 60
        
        # Física
        self.speed = settings.enemy_base_speed
        self.target_speed = settings.enemy_base_speed
        self.distance_to_player = 0
        
        # Física de salto
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = True
        
        # Hitbox de colisión
        self.hitbox = pygame.Rect(
            self.rect.x + 15,
            self.rect.y + 20,
            self.rect.width - 30,
            self.rect.height - 20
        )
        
    def update(self, difficulty_multiplier=1.0):
        """Actualiza la posición y estado del enemigo."""
        # Actualizar animación
        self.current_frame += self.animation_speed * difficulty_multiplier
        if self.current_frame >= len(self.running_frames):
            self.current_frame = 0
        self.image = self.running_frames[int(self.current_frame)]
        
        # Calcular distancia al jugador
        self.distance_to_player = self.player.rect.x - self.rect.x
        
        # Lógica de persecución por zonas
        if self.distance_to_player > 400:
            self.target_speed = self.settings.enemy_base_speed * self.settings.enemy_catch_up_speed * difficulty_multiplier
        elif self.distance_to_player > self.settings.enemy_target_distance:
            multiplier = 1 + ((self.distance_to_player - self.settings.enemy_target_distance) / 400)
            self.target_speed = self.settings.enemy_base_speed * multiplier * difficulty_multiplier
        elif self.distance_to_player < 100:
            self.target_speed = self.settings.enemy_base_speed * 0.9 * difficulty_multiplier
        else:
            self.target_speed = self.settings.enemy_base_speed * difficulty_multiplier
        
        # Transición suave de velocidad
        if self.speed < self.target_speed:
            self.speed += self.settings.enemy_acceleration
        elif self.speed > self.target_speed:
            self.speed -= self.settings.enemy_acceleration * 0.5
        
        # Mover al enemigo
        self.rect.x += self.speed
        
        # Aplicar gravedad al perro
        self.velocity_y += 0.65
        if self.velocity_y > 15:
            self.velocity_y = 15
        
        self.rect.y += self.velocity_y
        
        # Colisión con suelo - MANTENERLO PEGADO AL SUELO
        if self.rect.bottom >= self.settings.ground_level:
            self.rect.bottom = self.settings.ground_level + 60  # PEGADO AL SUELO
            self.velocity_y = 0
            self.is_jumping = False
            self.on_ground = True
        else:
            self.on_ground = False
        
        # Actualizar hitbox
        self.hitbox.x = self.rect.x + 15
        self.hitbox.y = self.rect.y + 20
    
    def jump(self):
        """Hace que el perro salte"""
        if self.on_ground:
            self.velocity_y = -12
            self.is_jumping = True
            self.on_ground = False
    
    def draw(self, screen):
        """Dibuja el enemigo en pantalla."""
        screen.blit(self.image, self.rect)
        
        # Efecto visual de proximidad
        if self.distance_to_player < 120:
            alpha = int(100 * (1 - self.distance_to_player / 120))
            shadow = pygame.Surface((self.rect.width, self.rect.height))
            shadow.set_alpha(alpha)
            shadow.fill((255, 0, 0))
            screen.blit(shadow, self.rect)
    
    def check_collision(self, player):
        """Verifica si el enemigo ha colisionado con el jugador."""
        return self.hitbox.colliderect(player.hitbox)
