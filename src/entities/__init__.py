# import pygame
# from src.core.utils import load_animation_frames

# class Enemy(pygame.sprite.Sprite):
#     """Perro perseguidor con IA balanceada y coherente"""
#     def __init__(self, settings, x, y, player):
#         super().__init__()
#         self.settings = settings
#         self.player = player
        
#         print("\n=== CARGANDO SPRITES DEL PERRO ===")
#         self.running_frames = load_animation_frames(
#             "assets/images/dog", 9, (110, 100), start_index=1
#         )
        
#         self.current_frame = 0
#         self.animation_speed = 0.20
#         self.image = self.running_frames[0]
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.bottom = y
        
#         # Física
#         self.speed = settings.enemy_base_speed
#         self.target_speed = settings.enemy_base_speed
#         self.distance_to_player = 0
        
#         # Hitbox
#         self.hitbox = pygame.Rect(
#             self.rect.x + 15,
#             self.rect.y + 20,
#             self.rect.width - 30,
#             self.rect.height - 20
#         )
        
#     def update(self, difficulty_multiplier=1.0):
#         """IA de persecución inteligente y balanceada"""
#         self.current_frame += self.animation_speed * difficulty_multiplier
#         if self.current_frame >= len(self.running_frames):
#             self.current_frame = 0
#         self.image = self.running_frames[int(self.current_frame)]
        
#         self.distance_to_player = self.player.rect.x - self.rect.x
        
#         # Sistema de persecución por zonas
#         if self.distance_to_player > 400:
#             # Zona 1: Muy lejos - acelerar fuerte
#             self.target_speed = self.settings.enemy_base_speed * self.settings.enemy_catch_up_speed * difficulty_multiplier
#         elif self.distance_to_player > self.settings.enemy_target_distance:
#             # Zona 2: Lejos - acelerar gradualmente
#             multiplier = 1 + ((self.distance_to_player - self.settings.enemy_target_distance) / 400)
#             self.target_speed = self.settings.enemy_base_speed * multiplier * difficulty_multiplier
#         elif self.distance_to_player < 100:
#             # Zona 3: Muy cerca - ralentizar
#             self.target_speed = self.settings.enemy_base_speed * 0.9 * difficulty_multiplier
#         else:
#             # Zona 4: Distancia ideal - velocidad normal
#             self.target_speed = self.settings.enemy_base_speed * difficulty_multiplier
        
#         # Transición suave de velocidad
#         if self.speed < self.target_speed:
#             self.speed += self.settings.enemy_acceleration
#         elif self.speed > self.target_speed:
#             self.speed -= self.settings.enemy_acceleration * 0.5
        
#         # Límites
#         max_speed = self.settings.enemy_max_speed * difficulty_multiplier
#         self.speed = max(self.settings.enemy_base_speed * 0.7, min(self.speed, max_speed))
        
#         # Movimiento
#         self.rect.x += self.speed
#         self.rect.bottom = self.settings.ground_level
        
#         # Actualizar hitbox
#         self.hitbox.x = self.rect.x + 15
#         self.hitbox.y = self.rect.y + 20
    
#     def draw(self, screen):
#         """Dibuja al enemigo"""
#         screen.blit(self.image, self.rect)
        
#         if self.distance_to_player < 150:
#             alpha = int(120 * (1 - self.distance_to_player / 150))
#             shadow = pygame.Surface((self.rect.width, self.rect.height))
#             shadow.set_alpha(alpha)
#             shadow.fill((255, 0, 0))
#             screen.blit(shadow, self.rect)
    
#     def check_collision(self, player):
#         """Verifica colisión"""
#         return self.hitbox.colliderect(player.hitbox)
