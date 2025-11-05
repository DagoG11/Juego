import pygame

class MainMenu:
    """
    Menú principal del juego.
    
    Pantalla de inicio que muestra el título, controles
    y permite iniciar el juego.
    """
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        
        # Fuentes para diferentes elementos
        self.title_font = pygame.font.Font(None, 84)
        self.menu_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 28)
        
    def handle_events(self, event):
        """
        Maneja los eventos de entrada del menú.
        
        Args:
            event: Evento de pygame a procesar
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.start_game()
    
    def update(self):
        """Actualiza el estado del menú (sin lógica activa)"""
        pass
    
    def draw(self, screen):
        """
        Dibuja el menú en pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        screen.fill(self.settings.bg_color)
        
        # Título principal con efecto de sombra
        title_text = self.title_font.render("DOGRUNNER", True, self.settings.yellow)
        title_shadow = self.title_font.render("DOGRUNNER", True, self.settings.black)
        title_rect = title_text.get_rect(center=(self.settings.screen_width // 2, 120))
        shadow_rect = title_shadow.get_rect(center=(self.settings.screen_width // 2 + 3, 123))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Subtítulo descriptivo
        subtitle_text = self.small_font.render("¡Escapa del perro feroz!", True, self.settings.red)
        subtitle_rect = subtitle_text.get_rect(center=(self.settings.screen_width // 2, 200))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Instrucción para iniciar
        start_text = self.menu_font.render("Presiona ESPACIO para comenzar", True, self.settings.white)
        start_shadow = self.menu_font.render("Presiona ESPACIO para comenzar", True, self.settings.black)
        start_rect = start_text.get_rect(center=(self.settings.screen_width // 2, 320))
        shadow_start_rect = start_shadow.get_rect(center=(self.settings.screen_width // 2 + 2, 322))
        screen.blit(start_shadow, shadow_start_rect)
        screen.blit(start_text, start_rect)
        
        # Título de controles
        controls_title = self.menu_font.render("CONTROLES:", True, self.settings.orange)
        controls_title_rect = controls_title.get_rect(center=(self.settings.screen_width // 2, 400))
        screen.blit(controls_title, controls_title_rect)
        
        # Lista de controles
        controls = [
            "ESPACIO o ↑ = Saltar",
            "← = Moverse a la izquierda",
            "→ = Moverse a la derecha",
            "",
            "¡Corre sin parar y evita los obstáculos!"
        ]
        
        y_offset = 450
        for control in controls:
            if control:
                control_text = self.small_font.render(control, True, self.settings.black)
                control_rect = control_text.get_rect(center=(self.settings.screen_width // 2, y_offset))
                screen.blit(control_text, control_rect)
            y_offset += 35
