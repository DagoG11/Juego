import pygame
from src.core.utils import load_animation_frames

class Enemy(pygame.sprite.Sprite):
    """
    Clase del enemigo perseguidor (Perro) con sistema de boost inteligente.
    
    - Persigue al jugador de forma natural
    - Salta automáticamente cajas
    - Recibe boosts cuando el jugador choca cajas
    - Boost de emergencia cuando está muy cerca y jugador ralentizado
    """

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
        self.rect.bottom = self.settings.ground_level + 60

        # Física
        self.speed = settings.enemy_base_speed
        self.target_speed = settings.enemy_base_speed
        self.distance_to_player = 0
        
        # Sistema de boost temporal
        self.temporary_boost = 1.0
        self.boost_decay = 0.98  # El boost se reduce gradualmente

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

    def apply_catchup_boost(self, boost_amount):
        """Aplica un boost temporal de velocidad al perro cuando está cerca"""
        self.temporary_boost = max(self.temporary_boost, boost_amount)

    def update(self, difficulty_multiplier=1.0):
        """Actualiza la posición y estado del enemigo."""
        # Actualizar animación
        self.current_frame += self.animation_speed * difficulty_multiplier
        if self.current_frame >= len(self.running_frames):
            self.current_frame = 0
        self.image = self.running_frames[int(self.current_frame)]

        # Calcular distancia al jugador
        self.distance_to_player = self.player.rect.x - self.rect.x

        # Lógica de persecución adaptativa
        if self.distance_to_player > 400:
            # Muy lejos, acelerar agresivamente
            self.target_speed = self.settings.enemy_base_speed * self.settings.enemy_catch_up_speed * difficulty_multiplier
        elif self.distance_to_player > self.settings.enemy_target_distance:
            # Distancia media, acelerar proporcionalmente a qué tan lejos está
            multiplier = 1.2 + ((self.distance_to_player - self.settings.enemy_target_distance) / 300)
            self.target_speed = self.settings.enemy_base_speed * multiplier * difficulty_multiplier
        elif self.distance_to_player < 100:
            # Muy cerca, mantener velocidad constante (no pasar al jugador)
            self.target_speed = self.settings.enemy_base_speed * 0.95 * difficulty_multiplier
        else:
            # Distancia ideal, mantener velocidad base
            self.target_speed = self.settings.enemy_base_speed * difficulty_multiplier

        # APLICAR BOOST TEMPORAL
        self.target_speed *= self.temporary_boost
        
        # Reducir boost gradualmente (decae naturalmente)
        if self.temporary_boost > 1.0:
            self.temporary_boost *= self.boost_decay
            if self.temporary_boost < 1.0:
                self.temporary_boost = 1.0

        # Transición suave de velocidad (responde rápido pero no es abrupto)
        if self.speed < self.target_speed:
            self.speed += self.settings.enemy_acceleration * 1.5
        elif self.speed > self.target_speed:
            self.speed -= self.settings.enemy_acceleration * 0.8

        # Mover al enemigo horizontalmente
        self.rect.x += self.speed

        # Aplicar gravedad
        self.velocity_y += 0.65
        if self.velocity_y > 15:
            self.velocity_y = 15
        self.rect.y += self.velocity_y

        # Colisión con suelo
        if self.rect.bottom >= self.settings.ground_level:
            self.rect.bottom = self.settings.ground_level + 60
            self.velocity_y = 0
            self.is_jumping = False
            self.on_ground = True
        else:
            self.on_ground = False

        # Actualizar hitbox
        self.hitbox.x = self.rect.x + 15
        self.hitbox.y = self.rect.y + 20

    def jump(self):
        """Hace que el perro salte (se llama automáticamente al detectar cajas)"""
        if self.on_ground:
            self.velocity_y = -12
            self.is_jumping = True
            self.on_ground = False

    def draw(self, screen):
        """Dibuja el enemigo en pantalla."""
        screen.blit(self.image, self.rect)


    def check_collision(self, player):
        """Verifica si el enemigo ha colisionado con el jugador (game over)."""
        return self.hitbox.colliderect(player.hitbox)
