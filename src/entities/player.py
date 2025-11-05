import pygame
from src.core.utils import load_animation_frames

class Player(pygame.sprite.Sprite):
    """Clase del jugador principal."""
    def __init__(self, settings, x, y):
        super().__init__()
        self.settings = settings
        
        print("\n=== CARGANDO SPRITES DEL JUGADOR ===")
        
        self.running_frames = load_animation_frames(
            "assets/images/player/running_movement", 9, settings.player_size, start_index=0, smoothing=settings.sprite_smoothing
        )
        
        # Animación
        self.current_frame = 0
        self.animation_speed = 0.3
        self.image = self.running_frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        # Física
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.on_ground = True
        self.can_jump = True
        
        # Direcciones
        self.moving_left = False
        self.moving_right = False
        self.facing_right = True
        
        # Estado
        self.is_dead = False
        self.invulnerable_timer = 0
        
        # Estados de ralentizado
        self.is_slowed_down_short = False
        self.slowdown_short_timer = 0
        
        self.is_slowed_down_long = False
        self.slowdown_long_timer = 0
        
        # Estado de parada
        self.is_stopped = False
        self.stop_timer = 0
        
        # Contador de cajas sin saltar - NO SE REINICIA HASTA PERDER
        self.boxes_dodged_count = 0
        
        # Hitbox de colisión
        self.hitbox = pygame.Rect(
            self.rect.x + 25,
            self.rect.y + 20,
            self.rect.width - 50,
            self.rect.height - 20
        )
        
    def update(self, difficulty_multiplier=1.0):
        """Actualiza el estado del jugador cada frame."""
        if self.is_dead:
            return
        
        # Movimiento lateral
        if self.moving_left:
            self.velocity_x = -self.settings.player_lateral_speed
            self.facing_right = False
        elif self.moving_right:
            self.velocity_x = self.settings.player_lateral_speed
            self.facing_right = True
        else:
            self.velocity_x *= 0.8
        
        # RALENTIZADO LARGO (Caja 2)
        if self.is_slowed_down_long:
            self.velocity_x *= self.settings.slowdown_speed_multiplier_2
            self.slowdown_long_timer -= 1
            if self.slowdown_long_timer <= 0:
                self.is_slowed_down_long = False
        # RALENTIZADO CORTO (Caja 1)
        elif self.is_slowed_down_short:
            self.velocity_x *= self.settings.slowdown_speed_multiplier_1
            self.slowdown_short_timer -= 1
            if self.slowdown_short_timer <= 0:
                self.is_slowed_down_short = False
        # DETENCIÓN (Caja 3)
        elif self.is_stopped:
            self.velocity_x = 0
            self.stop_timer -= 1
            if self.stop_timer <= 0:
                self.is_stopped = False
        
        # Aplicar movimiento lateral
        self.rect.x += int(self.velocity_x)
        
        # Límites de pantalla
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity_x = 0
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
            self.velocity_x = 0
        
        # Aplicar gravedad
        self.velocity_y += self.settings.gravity
        if self.velocity_y > self.settings.max_fall_speed:
            self.velocity_y = self.settings.max_fall_speed
        
        self.rect.y += self.velocity_y
        
        # Colisión con suelo
        if self.rect.bottom >= self.settings.ground_level:
            self.rect.bottom = self.settings.ground_level
            self.velocity_y = 0
            self.is_jumping = False
            self.on_ground = True
            self.can_jump = True
        else:
            self.on_ground = False
        
        # Actualizar animación
        self.current_frame += self.animation_speed * difficulty_multiplier
        if self.current_frame >= len(self.running_frames):
            self.current_frame = 0
        
        base_image = self.running_frames[int(self.current_frame)]
        if not self.facing_right:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image
        
        # Actualizar hitbox
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.y = self.rect.y + 20
        
        # Sistema de invulnerabilidad
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
    
    def jump(self):
        """Ejecuta un salto si el jugador está en el suelo"""
        if self.on_ground and self.can_jump and not self.is_dead:
            self.velocity_y = self.settings.player_jump_power
            self.is_jumping = True
            self.on_ground = False
            self.can_jump = False
    
    def hit_slowdown_short(self):
        """Caja 1: Ralentiza 2 segundos"""
        self.is_slowed_down_short = True
        self.slowdown_short_timer = self.settings.slowdown_duration_1
        self.invulnerable_timer = self.settings.slowdown_duration_1
    
    def hit_slowdown_long(self):
        """Caja 2: Ralentiza 4 segundos"""
        self.is_slowed_down_long = True
        self.slowdown_long_timer = self.settings.slowdown_duration_2
        self.invulnerable_timer = self.settings.slowdown_duration_2
    
    def hit_hard_obstacle(self):
        """Caja 3: Detiene completamente"""
        self.is_stopped = True
        self.stop_timer = self.settings.stop_duration
        self.invulnerable_timer = self.settings.stop_duration
        self.velocity_x = 0
    
    def increment_boxes_dodged(self):
        """Incrementa el contador de cajas sin saltar"""
        self.boxes_dodged_count += 1
    
    def reset_boxes_dodged(self):
        """Reinicia el contador cuando salta una caja"""
        self.boxes_dodged_count = 0
    
    def die(self):
        """Marca al jugador como muerto"""
        self.is_dead = True
    
    def draw(self, screen):
        """Dibuja el jugador en pantalla."""
        if self.invulnerable_timer > 0 and self.invulnerable_timer % 6 < 3:
            return
        
        screen.blit(self.image, self.rect)
