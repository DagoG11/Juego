import pygame
from src.core.utils import load_image


class MainMenu:
    """
    Menú principal del juego basado en start.png con botón PLAY encima.
    """

    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        
        # Cargar imagen start.png que ya tiene el título
        try:
            self.start_image = load_image(
                "assets/images/background/start",
                (self.settings.screen_width, self.settings.screen_height),
                smoothing=self.settings.sprite_smoothing
            )
        except Exception as e:
            self.start_image = None
            print(f"⚠️ No se pudo cargar la imagen start.png: {e}")
        
        # Fuentes para botón e instrucciones
        self.font_button = pygame.font.Font(None, 48)
        self.font_instructions = pygame.font.Font(None, 28)
        
        # Botón PLAY - posición fija en pantalla
        self.play_button_rect = pygame.Rect(
            self.settings.screen_width // 2 - 100,
            self.settings.screen_height - 150,
            200,
            60
        )
        
        self.blink_timer = 0  # Para parpadeo instrucciones

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            return 'start_game'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button_rect.collidepoint(event.pos):
                return 'start_game'
        return None

    def update(self):
        self.blink_timer += 1
        if self.blink_timer > 120:
            self.blink_timer = 0

    def draw(self, screen):
        if self.start_image:
            screen.blit(self.start_image, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Dibujar botón PLAY encima de la imagen
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.play_button_rect.collidepoint(mouse_pos)
        
        button_color = (255, 200, 50) if is_hover else (200, 100, 30)
        pygame.draw.rect(screen, button_color, self.play_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.play_button_rect, 3, border_radius=10)
        
        play_text = self.font_button.render("PLAY", True, (0, 0, 0))
        play_x = self.play_button_rect.centerx - play_text.get_width() // 2
        play_y = self.play_button_rect.centery - play_text.get_height() // 2
        screen.blit(play_text, (play_x, play_y))

        # Instrucciones que parpadean debajo del botón
        if self.blink_timer < 60:
            instructions = [
                "Presiona ESPACIO o haz clic en PLAY para comenzar",
                "",
                "Controles:",
                "ESPACIO / ↑ = Saltar",
                "← / → = Moverse",
            ]
            y_offset = self.settings.screen_height - 80
            for i, line in enumerate(instructions):
                inst_text = self.font_instructions.render(line, True, (255, 255, 255))
                inst_x = self.settings.screen_width // 2 - inst_text.get_width() // 2
                screen.blit(inst_text, (inst_x, y_offset + i * 30))
