import pygame

class Settings:
    """Configuración general del juego"""
    def __init__(self):
        # Pantalla
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.fps = 60
        
        # Jugador - Velocidad constante
        self.player_run_speed = 7.6
        self.player_lateral_speed = 6.0
        self.player_jump_power = -25
        self.gravity = 0.65
        self.max_fall_speed = 15
        
        # Enemigo - Perseguidor
        self.enemy_base_speed = 3.0
        self.enemy_acceleration = 0.01
        self.enemy_max_speed = 4.0
        self.enemy_catch_up_speed = 1.8
        self.enemy_distance_start = -300
        self.enemy_target_distance = 200
        self.enemy_catch_distance = 30
        
        # Mundo
        self.world_scroll_speed = 5.5
        
        # Obstáculos - MENOS FRECUENTES
        self.obstacle_spawn_distance = 600
        self.min_obstacle_distance = 400
        
        # Configuración de tamaños de cajas
        self.box_sizes = {
            1: (110, 110),    # Caja 1: Ralentiza 2 segundos
            2: (130, 130),    # Caja 2: Ralentiza 4 segundos
            3: (130, 130),    # Caja 3: Detiene por completo
        }
        
        # TAMAÑOS DE PERSONAJES
        self.player_size = (180, 180)      # Tamaño del jugador
        self.enemy_size = (175, 175)       # Tamaño del perro
        
        # SUAVIZADO DE SPRITES
        self.sprite_smoothing = False
        
        # ========================================
        # CONFIGURACIÓN DE EFECTOS POR CAJA
        # ========================================
        # Caja 1: Ralentiza 2 segundos
        self.slowdown_speed_multiplier_1 = 0.3  # 30% de velocidad
        self.slowdown_duration_1 = 120  # 120 frames = 2 segundos
        
        # Caja 2: Ralentiza 4 segundos
        self.slowdown_speed_multiplier_2 = 0.2  # 20% de velocidad
        self.slowdown_duration_2 = 240  # 240 frames = 4 segundos
        
        # Caja 3: Detiene por completo
        self.stop_duration = 30  # 120 frames = 2 segundos (detenido)
        
        # ========================================
        # SISTEMA DE CAJAS SALTADAS
        # ========================================
        self.boxes_dodged_limit = 5  # Límite de cajas sin saltar
        
        # Dificultad progresiva
        self.difficulty_increase_rate = 0.0003
        self.max_difficulty_multiplier = 1.5
        
        # Físicas
        self.ground_level = 600
        self.friction = 0.85
        
        # Colores
        self.bg_color = (135, 206, 235)
        self.ground_color = (101, 67, 33)
        self.grass_color = (34, 139, 34)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 215, 0)
        self.orange = (255, 165, 0)
