import pygame
import sys
from src.scenes.level1 import Level1
from src.scenes.main_menu import MainMenu

class Game:
    """
    Clase principal del juego.
    
    Gestiona el ciclo principal del juego, estados (menú, jugando, game over)
    y la transición entre ellos.
    """
    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.set_mode(
            (settings.screen_width, settings.screen_height)
        )
        pygame.display.set_caption("DOGRUNNER")
        self.clock = pygame.time.Clock()
        
        # Estados del juego
        self.state = "menu"
        self.score = 0
        self.high_score = 0
        
        # Escenas del juego
        self.main_menu = MainMenu(self)
        self.level = None
        
    def run(self):
        """
        Ciclo principal del juego.
        
        Maneja eventos, actualiza lógica y dibuja en pantalla
        a 60 FPS constantes.
        """
        running = True
        
        while running:
            self.clock.tick(self.settings.fps)
            
            # Procesar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.state == "menu":
                    self.main_menu.handle_events(event)
                elif self.state == "playing":
                    self.level.handle_events(event)
                elif self.state == "game_over":
                    self.handle_game_over_events(event)
            
            # Actualizar lógica
            if self.state == "menu":
                self.main_menu.update()
            elif self.state == "playing":
                self.level.update()
                if self.level.game_over:
                    self.state = "game_over"
                    if self.score > self.high_score:
                        self.high_score = self.score
            
            # Renderizar pantalla
            if self.state == "menu":
                self.main_menu.draw(self.screen)
            elif self.state == "playing":
                self.level.draw(self.screen)
            elif self.state == "game_over":
                self.draw_game_over()
            
            pygame.display.flip()
    
    def start_game(self):
        """Inicia una nueva partida del nivel 1"""
        self.state = "playing"
        self.score = 0
        self.level = Level1(self)
        print("\n" + "="*60)
        print("🎮 JUEGO INICIADO")
        print("="*60 + "\n")
    
    def handle_game_over_events(self, event):
        """
        Maneja eventos en la pantalla de game over.
        
        Args:
            event: Evento de pygame a procesar
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.state = "menu"
    
    def draw_game_over(self):
        """Dibuja la pantalla de game over con puntaje y opciones"""
        self.screen.fill(self.settings.black)
        
        font_big = pygame.font.Font(None, 74)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # Título de game over
        game_over_text = font_big.render("GAME OVER", True, self.settings.red)
        game_over_rect = game_over_text.get_rect(
            center=(self.settings.screen_width // 2, 150)
        )
        self.screen.blit(game_over_text, game_over_rect)
        
        # Mensaje de captura
        caught_text = font_medium.render("¡El perro te atrapó!", True, self.settings.orange)
        caught_rect = caught_text.get_rect(
            center=(self.settings.screen_width // 2, 230)
        )
        self.screen.blit(caught_text, caught_rect)
        
        # Puntaje de la partida
        score_text = font_small.render(
            f"Distancia recorrida: {int(self.score)} m", 
            True, self.settings.white
        )
        score_rect = score_text.get_rect(
            center=(self.settings.screen_width // 2, 310)
        )
        self.screen.blit(score_text, score_rect)
        
        # Récord personal
        if self.high_score > 0:
            high_score_text = font_small.render(
                f"Récord: {int(self.high_score)} m", 
                True, self.settings.yellow
            )
            high_score_rect = high_score_text.get_rect(
                center=(self.settings.screen_width // 2, 360)
            )
            self.screen.blit(high_score_text, high_score_rect)
        
        # Instrucciones de reinicio
        restart_text = font_small.render(
            "Presiona ESPACIO para reintentar", 
            True, self.settings.white
        )
        restart_rect = restart_text.get_rect(
            center=(self.settings.screen_width // 2, 440)
        )
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = font_small.render(
            "Presiona ESC para volver al menú", 
            True, self.settings.white
        )
        menu_rect = menu_text.get_rect(
            center=(self.settings.screen_width // 2, 490)
        )
        self.screen.blit(menu_text, menu_rect)
