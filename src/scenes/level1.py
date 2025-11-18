import pygame
import random
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.obstacle import Obstacle
from src.core.utils import load_image

class Level1:
    """
    Nivel principal del juego.
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
        self.day_night_timer = 0
        self.day_night_cycle_duration = 3600  # 60 seg * 60 fps
        self.is_day = True
        self.load_backgrounds()
        self.game_over = False
        self.distance = 0
        self.difficulty_multiplier = 1.0
        self.enemy_boost_multiplier = 1.0
        self.consecutive_hits = 0
        self.obstacles_passed = {}
        self.dust_particles = []
        self.impact_particles = []
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        self.font_big = pygame.font.Font(None, 48)

    def load_backgrounds(self):
        try:
            self.bg_day = load_image(
                "assets/images/background/day/day",
                (self.settings.screen_width, self.settings.screen_height),
                smoothing=self.settings.sprite_smoothing
            )
        except:
            self.bg_day = None
        try:
            self.bg_night = load_image(
                "assets/images/background/night/night",
                (self.settings.screen_width, self.settings.screen_height),
                smoothing=self.settings.sprite_smoothing
            )
        except:
            self.bg_night = None

    def spawn_obstacle(self):
        spawn_x = self.last_obstacle_x + random.randint(
            self.settings.min_obstacle_distance + 100,
            self.settings.obstacle_spawn_distance + 200
        )
        obstacle = Obstacle(self.settings, spawn_x)
        self.obstacles.add(obstacle)
        self.last_obstacle_x = spawn_x

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                self.player.jump()

    def update(self):
        if not self.game_over:
            keys = pygame.key.get_pressed()
            self.player.moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
            self.player.moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

            # Actualizar ciclo día/noche
            self.day_night_timer += 1
            if self.day_night_timer >= self.day_night_cycle_duration:
                self.day_night_timer = 0
                self.is_day = not self.is_day

            self.difficulty_multiplier += self.settings.difficulty_increase_rate
            if self.difficulty_multiplier > self.settings.max_difficulty_multiplier:
                self.difficulty_multiplier = self.settings.max_difficulty_multiplier

            base_scroll_speed = self.settings.world_scroll_speed * self.difficulty_multiplier

            self.player.update(self.difficulty_multiplier)

            # CAMARA QUE SIGUE AL PLAYER
            target_x = self.settings.screen_width // 3
            diff_x = self.player.rect.x - target_x
            scroll_speed = diff_x if diff_x > 0 else 0

            self.bg_scroll -= scroll_speed * 0.5
            self.bg_scroll2 -= scroll_speed * 0.5
            if self.bg_scroll <= -self.settings.screen_width:
                self.bg_scroll = self.settings.screen_width
            if self.bg_scroll2 <= -self.settings.screen_width:
                self.bg_scroll2 = self.settings.screen_width

            self.player.rect.x = target_x

            for obstacle in self.obstacles:
                distance_to_obstacle = obstacle.rect.x - self.enemy.rect.x
                if 30 < distance_to_obstacle < 200:
                    if self.enemy.on_ground:
                        self.enemy.jump()
                    break
                if self.enemy.hitbox.colliderect(obstacle.hitbox):
                    self.enemy.speed = -5
                    self.enemy.target_speed = -5
                    break

            distance_to_player = self.player.rect.x - self.enemy.rect.x
            if (self.player.is_stopped or self.player.is_slowed_down_long or
                    self.player.is_slowed_down_short):
                if distance_to_player < 150:
                    self.enemy.apply_catchup_boost(2.5)
                elif distance_to_player < 250:
                    self.enemy.apply_catchup_boost(1.5)

            self.enemy.update(self.difficulty_multiplier * self.enemy_boost_multiplier)
            self.enemy.rect.x -= scroll_speed

            if self.enemy.rect.right < -50:
                self.enemy.rect.x = -80
            elif self.enemy.rect.left > self.settings.screen_width + 100:
                self.enemy.rect.x = -80

            obstacles_to_remove = []
            for obstacle in self.obstacles:
                obstacle.rect.x -= scroll_speed
                obstacle.update(0)
                if obstacle.hitbox.colliderect(self.player.hitbox):
                    hit_registered = False
                    if obstacle.is_hard:
                        if not self.player.is_stopped:
                            self.player.hit_hard_obstacle()
                            hit_registered = True
                            self.create_impact_particles(obstacle.rect.centerx, obstacle.rect.centery)
                    elif obstacle.is_slowdown_short:
                        if not self.player.is_slowed_down_short:
                            self.player.hit_slowdown_short()
                            hit_registered = True
                            self.create_impact_particles(obstacle.rect.centerx, obstacle.rect.centery)
                    elif obstacle.is_slowdown_long:
                        if not self.player.is_slowed_down_long:
                            self.player.hit_slowdown_long()
                            hit_registered = True
                            self.create_impact_particles(obstacle.rect.centerx, obstacle.rect.centery)
                    if hit_registered:
                        self.consecutive_hits += 1
                        self.player.boxes_dodged_count += 1
                        boost_increment = 0.15 * self.consecutive_hits
                        self.enemy_boost_multiplier += boost_increment
                        if self.player.boxes_dodged_count >= 4:
                            self.enemy_boost_multiplier = 3.0
                        self.obstacles_passed[id(obstacle)] = 'hit'
                elif obstacle.rect.right < self.player.rect.left:
                    obstacle_id = id(obstacle)
                    if obstacle_id not in self.obstacles_passed:
                        if self.enemy_boost_multiplier > 1.0:
                            self.enemy_boost_multiplier = max(1.0, self.enemy_boost_multiplier - 1.0)
                        self.consecutive_hits = max(0, self.consecutive_hits - 1)
                    self.obstacles_passed[obstacle_id] = True
                    obstacles_to_remove.append(obstacle)

            for obstacle in obstacles_to_remove:
                self.obstacles.remove(obstacle)

            if self.last_obstacle_x - scroll_speed < self.settings.screen_width + 200:
                self.spawn_obstacle()
            self.last_obstacle_x -= scroll_speed

            self.bg_scroll -= scroll_speed * 0.5
            self.bg_scroll2 -= scroll_speed * 0.5
            if self.bg_scroll <= -self.settings.screen_width:
                self.bg_scroll = self.settings.screen_width
            if self.bg_scroll2 <= -self.settings.screen_width:
                self.bg_scroll2 = self.settings.screen_width

            # Limitar al jugador para que no quede pegado a la esquina
            if self.player.rect.left < 20:
                self.player.rect.left = 20
            elif self.player.rect.right > self.settings.screen_width - 20:
                self.player.rect.right = self.settings.screen_width - 20

            # Limitar al enemigo para que no quede en esquina
            if self.enemy.rect.left < 10:
                self.enemy.rect.left = 10
            elif self.enemy.rect.right > self.settings.screen_width - 10:
                self.enemy.rect.right = self.settings.screen_width - 10

            if scroll_speed > 0:
                self.distance += 0.1 * self.difficulty_multiplier
                self.game.score = self.distance
            if scroll_speed > 0 and random.random() < 0.4 and self.player.on_ground:
                self.create_dust_particle()

            self.update_dust_particles(scroll_speed)
            self.update_impact_particles()
            if self.enemy.check_collision(self.player):
                self.game_over = True

    # Métodos para partículas y HUD (similares a tu código original)

    def create_dust_particle(self):
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
        for particle in self.dust_particles[:]:
            particle['x'] += particle['velocity_x'] - scroll_speed
            particle['y'] += particle['velocity_y']
            particle['life'] -= 1
            particle['size'] -= 0.2
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.dust_particles.remove(particle)

    def update_impact_particles(self):
        for particle in self.impact_particles[:]:
            particle['x'] += particle['velocity_x']
            particle['y'] += particle['velocity_y']
            particle['velocity_y'] += 0.5
            particle['life'] -= 1
            particle['size'] -= 0.15
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.impact_particles.remove(particle)

    def draw(self, screen):
        screen.fill(self.settings.bg_color)

        bg = self.bg_day if self.is_day else self.bg_night
        if bg:
            screen.blit(bg, (self.bg_scroll, 0))
            screen.blit(bg, (self.bg_scroll2, 0))
        else:
            screen.fill((135, 206, 235) if self.is_day else (25, 25, 50))

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

        if self.enemy_boost_multiplier > 1.0:
            boost_text = self.font_small.render(
                f"Velocidad perro: {self.enemy_boost_multiplier:.1f}x",
                True, self.settings.red
            )
            screen.blit(boost_text, (10, 85))

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
