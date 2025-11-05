import pygame
import random
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.obstacle import Obstacle
from src.core.utils import load_image

class Level1:
    """
    Nivel principal del juego.
    
    SISTEMA DE DESAFÍO:
    - Cada 4 cajas sin saltar: PERRO ACCELERA AL MÁXIMO Y PIERDES
    - Perro salta automáticamente las cajas
    """
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        
        self.player = Player(self.settings, 300, self.settings.ground_level)
        
        self.enemy = Enemy(
            self.settings, 
            self.player.rect.x + self.settings.enemy_distance_start,
            self.settings.ground_level,
            self.player
        )
        
        self.obstacles = pygame.sprite.Group()
        self.last_obstacle_x = self.settings.screen_width + 300
        
        for i in range(2):
            self.spawn_obstacle()
        
        self.bg_scroll = 0
        self.bg_scroll2 = self.settings.screen_width
        self.load_backgrounds()
        
        self.game_over = False
        self.distance = 0
        self.difficulty_multiplier = 1.0
        
        self.dust_particles = []
        self.impact_particles = []
        
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        self.font_big = pygame.font.Font(None, 48)
        
    def load_backgrounds(self):
        """Carga las imágenes de fondo del nivel"""
        try:
            self.bg_desert = load_image(
                "assets/images/background/desert/desert (1)", 
                (self.settings.screen_width, self.settings.screen_height),
                smoothing=self.settings.sprite_smoothing
            )
        except:
            self.bg_desert = None
    
    def spawn_obstacle(self):
        """Genera un nuevo obstáculo con imagen aleatoria de caja"""
        spawn_x = self.last_obstacle_x + random.randint(
            self.settings.min_obstacle_distance,
            self.settings.obstacle_spawn_distance
        )
        
        obstacle = Obstacle(self.settings, spawn_x)
        self.obstacles.add(obstacle)
        
        self.last_obstacle_x = spawn_x
    
    def handle_events(self, event):
        """Maneja los eventos de entrada del nivel."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                self.player.jump()
    
    def update(self):
        """Actualiza la lógica del nivel cada frame"""
        if not self.game_over:
            # Control de movimiento lateral
            keys = pygame.key.get_pressed()
            self.player.moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
            self.player.moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            
            # Incrementar dificultad progresivamente
            self.difficulty_multiplier += self.settings.difficulty_increase_rate
            if self.difficulty_multiplier > self.settings.max_difficulty_multiplier:
                self.difficulty_multiplier = self.settings.max_difficulty_multiplier
            
            # Calcular velocidad de scroll constante
            scroll_speed = self.settings.world_scroll_speed * self.difficulty_multiplier
            
            # Actualizar jugador
            self.player.update(self.difficulty_multiplier)
            
            # Hacer que el perro salte sobre cajas cercanas - RANGO AMPLIADO
            for obstacle in self.obstacles:
                distance_to_obstacle = obstacle.rect.x - self.enemy.rect.x
                if 30 < distance_to_obstacle < 200:  # RANGO AMPLIADO
                    if self.enemy.on_ground:
                        self.enemy.jump()
                        print(f"🐕 ¡Perro salta caja! Distancia: {distance_to_obstacle}")
                    break
            
            # Actualizar enemigo
            self.enemy.update(self.difficulty_multiplier)
            
            # Compensar scroll del mundo en el enemigo
            self.enemy.rect.x -= scroll_speed
            
            # Reposicionar enemigo si sale de pantalla
            if self.enemy.rect.right < -50:
                self.enemy.rect.x = self.player.rect.x + self.settings.enemy_distance_start
            
            # Actualizar obstáculos
            for obstacle in self.obstacles:
                obstacle.update(scroll_speed)
                
                # Detectar colisión con jugador
                if obstacle.hitbox.colliderect(self.player.hitbox):
                    if obstacle.is_hard:
                        # Caja 3: SIEMPRE detiene completamente
                        if not self.player.is_stopped:
                            self.player.hit_hard_obstacle()
                            self.player.reset_boxes_dodged()
                            self.create_impact_particles(obstacle.rect.centerx, obstacle.rect.centery)
                            print("💥 ¡Caja 3 - DETENIDO!")
                    elif obstacle.is_slowdown_short:
                        # Caja 1: SIEMPRE ralentiza 2 segundos
                        if not self.player.is_slowed_down_short:
                            self.player.hit_slowdown_short()
                            self.player.reset_boxes_dodged()
                            self.create_impact_particles(obstacle.rect.centerx, obstacle.rect.centery)
                            print("⚡ ¡Caja 1 - RALENTIZADO 2 SEG!")
                    elif obstacle.is_slowdown_long:
                        # Caja 2: SIEMPRE ralentiza 4 segundos
                        if not self.player.is_slowed_down_long:
                            self.player.hit_slowdown_long()
                            self.player.reset_boxes_dodged()
                            self.create_impact_particles(obstacle.rect.centerx, obstacle.rect.centery)
                            print("⚡⚡ ¡Caja 2 - RALENTIZADO 4 SEG!")
                
                # Eliminar obstáculos fuera de pantalla
                if obstacle.rect.right < -50:
                    # Si se pasó la caja SIN chocar, incrementar contador
                    if obstacle.rect.right < self.player.rect.left:
                        self.player.increment_boxes_dodged()
                        print(f"📦 Cajas sin saltar: {self.player.boxes_dodged_count}/4")
                        
                        # VERIFICAR SI ALCANZÓ 4 CAJAS SIN SALTAR
                        if self.player.boxes_dodged_count >= self.settings.boxes_dodged_limit:
                            print(f"🔥 ¡¡¡ 4 CAJAS SIN SALTAR (TOTAL: {self.player.boxes_dodged_count}) !!!")
                            print("🐕 ¡¡¡ EL PERRO ACCELERA AL MÁXIMO Y TE ATRAPA !!!")
                            
                            # EL PERRO ACCELERA A VELOCIDAD EXTREMA
                            velocidad_perro = self.settings.enemy_max_speed * (5 + (self.player.boxes_dodged_count // 4))
                            self.enemy.speed = velocidad_perro
                            self.enemy.target_speed = velocidad_perro
                            
                            # GAME OVER INMEDIATO
                            self.game_over = True
                    
                    self.obstacles.remove(obstacle)
            
            # Generar nuevos obstáculos
            if self.last_obstacle_x - scroll_speed < self.settings.screen_width + 200:
                self.spawn_obstacle()
            
            self.last_obstacle_x -= scroll_speed
            
            # Scroll del fondo (parallax)
            self.bg_scroll -= scroll_speed * 0.5
            self.bg_scroll2 -= scroll_speed * 0.5
            
            if self.bg_scroll <= -self.settings.screen_width:
                self.bg_scroll = self.settings.screen_width
            if self.bg_scroll2 <= -self.settings.screen_width:
                self.bg_scroll2 = self.settings.screen_width
            
            # Incrementar distancia recorrida
            self.distance += 0.1 * self.difficulty_multiplier
            self.game.score = self.distance
            
            # Crear partículas de polvo
            if random.random() < 0.4 and self.player.on_ground:
                self.create_dust_particle()
            
            # Actualizar sistemas de partículas
            self.update_dust_particles(scroll_speed)
            self.update_impact_particles()
            
            # Verificar captura por el enemigo
            if self.enemy.check_collision(self.player):
                self.game_over = True
    
    def create_dust_particle(self):
        """Crea una partícula de polvo detrás del jugador"""
        particle = {
            'x': self.player.rect.left + random.randint(-10, 10),
            'y': self.player.rect.bottom - 5,
            'size': random.randint(4, 8),
            'life': 25,
            'velocity_x': -random.randint(1, 3),
            'velocity_y': -random.randint(1, 3)
        }
        self.dust_particles.append(particle)
    
    def create_impact_particles(self, x, y):
        """Crea partículas de impacto al chocar con obstáculo."""
        for _ in range(8):
            particle = {
                'x': x,
                'y': y,
                'size': random.randint(3, 6),
                'life': 20,
                'velocity_x': random.randint(-5, 5),
                'velocity_y': random.randint(-8, -3),
                'color': random.choice([(255, 100, 0), (255, 200, 0), (255, 50, 0)])
            }
            self.impact_particles.append(particle)
    
    def update_dust_particles(self, scroll_speed):
        """Actualiza el sistema de partículas de polvo"""
        for particle in self.dust_particles[:]:
            particle['x'] += particle['velocity_x'] - scroll_speed
            particle['y'] += particle['velocity_y']
            particle['life'] -= 1
            particle['size'] -= 0.2
            
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.dust_particles.remove(particle)
    
    def update_impact_particles(self):
        """Actualiza el sistema de partículas de impacto"""
        for particle in self.impact_particles[:]:
            particle['x'] += particle['velocity_x']
            particle['y'] += particle['velocity_y']
            particle['velocity_y'] += 0.5
            particle['life'] -= 1
            particle['size'] -= 0.15
            
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.impact_particles.remove(particle)
    
    def draw(self, screen):
        """Dibuja todos los elementos del nivel en pantalla."""
        screen.fill(self.settings.bg_color)
        
        if self.bg_desert:
            screen.blit(self.bg_desert, (self.bg_scroll, 0))
            screen.blit(self.bg_desert, (self.bg_scroll2, 0))
        
        pygame.draw.rect(screen, self.settings.ground_color, 
                        (0, self.settings.ground_level, 
                         self.settings.screen_width, 
                         self.settings.screen_height - self.settings.ground_level))
        
        pygame.draw.rect(screen, self.settings.grass_color, 
                        (0, self.settings.ground_level, 
                         self.settings.screen_width, 5))
        
        for particle in self.dust_particles:
            if particle['size'] > 0:
                alpha_value = int((particle['life'] / 25) * 150)
                dust_surface = pygame.Surface((int(particle['size']), int(particle['size'])))
                dust_surface.set_alpha(alpha_value)
                dust_surface.fill((200, 180, 150))
                screen.blit(dust_surface, (particle['x'], particle['y']))
        
        for particle in self.impact_particles:
            if particle['size'] > 0:
                alpha_value = int((particle['life'] / 20) * 200)
                impact_surface = pygame.Surface((int(particle['size']), int(particle['size'])))
                impact_surface.set_alpha(alpha_value)
                impact_surface.fill(particle['color'])
                screen.blit(impact_surface, (particle['x'], particle['y']))
        
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        self.player.draw(screen)
        self.enemy.draw(screen)
        
        self.draw_hud(screen)
    
    def draw_hud(self, screen):
        """Dibuja la interfaz de usuario (HUD)"""
        # Distancia recorrida
        distance_text = self.font.render(
            f"Distancia: {int(self.distance)} m", 
            True, self.settings.white
        )
        distance_shadow = self.font.render(
            f"Distancia: {int(self.distance)} m", 
            True, self.settings.black
        )
        screen.blit(distance_shadow, (12, 12))
        screen.blit(distance_text, (10, 10))
        
        # Contador de cajas sin saltar
        boxes_color = self.settings.red if self.player.boxes_dodged_count >= 3 else self.settings.orange
        boxes_text = self.font_small.render(
            f"Cajas sin saltar: {self.player.boxes_dodged_count}/4",
            True, boxes_color
        )
        boxes_shadow = self.font_small.render(
            f"Cajas sin saltar: {self.player.boxes_dodged_count}/4",
            True, self.settings.black
        )
        screen.blit(boxes_shadow, (12, 52))
        screen.blit(boxes_text, (10, 50))
        
        # Barra de peligro del enemigo
        distance_to_enemy = self.player.rect.x - self.enemy.rect.x
        if distance_to_enemy < 350:
            danger_level = max(0, min(1, 1 - (distance_to_enemy / 350)))
            bar_width = 200
            bar_height = 15
            bar_x = self.settings.screen_width - bar_width - 20
            bar_y = 20
            
            red_value = max(0, min(255, int(255 * danger_level)))
            green_value = max(0, min(255, int(255 * (1 - danger_level))))
            danger_color = (red_value, green_value, 0)
            
            pygame.draw.rect(screen, self.settings.white, 
                           (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
            pygame.draw.rect(screen, self.settings.black, 
                           (bar_x, bar_y, bar_width, bar_height))
            
            fill_width = max(0, min(bar_width, int(bar_width * danger_level)))
            pygame.draw.rect(screen, danger_color, 
                           (bar_x, bar_y, fill_width, bar_height))
            
            if distance_to_enemy < 120:
                warning_text = self.font_big.render("¡CORRE!", True, self.settings.red)
                warning_shadow = self.font_big.render("¡CORRE!", True, self.settings.black)
                screen.blit(warning_shadow, (bar_x + 22, bar_y + 27))
                screen.blit(warning_text, (bar_x + 20, bar_y + 25))
