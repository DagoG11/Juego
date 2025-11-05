import pygame

class HUD:
    """Heads-Up Display para mostrar información del juego en pantalla"""
    def __init__(self, settings):
        self.settings = settings
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        
    def draw_distance(self, screen, distance, x=10, y=10):
        """Dibuja la distancia recorrida"""
        distance_text = self.font_medium.render(
            f"Distancia: {int(distance)} m", 
            True, self.settings.white
        )
        distance_shadow = self.font_medium.render(
            f"Distancia: {int(distance)} m", 
            True, self.settings.black
        )
        screen.blit(distance_shadow, (x + 2, y + 2))
        screen.blit(distance_text, (x, y))
    
    def draw_speed(self, screen, speed, max_speed, x=10, y=50):
        """Dibuja el velocímetro"""
        speed_percent = int((speed / max_speed) * 100)
        speed_text = self.font_small.render(
            f"Velocidad: {speed_percent}%", 
            True, self.settings.yellow
        )
        screen.blit(speed_text, (x, y))
    
    def draw_danger_bar(self, screen, distance_to_enemy, max_distance=350):
        """Dibuja la barra de peligro del enemigo"""
        if distance_to_enemy >= max_distance:
            return
        
        danger_level = max(0, min(1, 1 - (distance_to_enemy / max_distance)))
        bar_width = 200
        bar_height = 15
        bar_x = self.settings.screen_width - bar_width - 20
        bar_y = 20
        
        # Calcular color (rojo a verde)
        red_value = max(0, min(255, int(255 * danger_level)))
        green_value = max(0, min(255, int(255 * (1 - danger_level))))
        danger_color = (red_value, green_value, 0)
        
        # Dibujar barra
        pygame.draw.rect(screen, self.settings.white, 
                       (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, self.settings.black, 
                       (bar_x, bar_y, bar_width, bar_height))
        
        fill_width = max(0, min(bar_width, int(bar_width * danger_level)))
        pygame.draw.rect(screen, danger_color, 
                       (bar_x, bar_y, fill_width, bar_height))
        
        # Advertencia si está muy cerca
        if distance_to_enemy < 150:
            warning_text = self.font_large.render("¡CORRE!", True, self.settings.red)
            warning_shadow = self.font_large.render("¡CORRE!", True, self.settings.black)
            warning_x = bar_x + bar_width // 2 - 60
            warning_y = bar_y + 25
            screen.blit(warning_shadow, (warning_x + 2, warning_y + 2))
            screen.blit(warning_text, (warning_x, warning_y))
    
    def draw_lives(self, screen, lives, x=10, y=90):
        """Dibuja las vidas del jugador (opcional)"""
        lives_text = self.font_small.render(f"Vidas: {lives}", True, self.settings.white)
        screen.blit(lives_text, (x, y))
    
    def draw_debug_info(self, screen, player, enemy):
        """Dibuja información de debug (opcional)"""
        debug_font = pygame.font.Font(None, 20)
        debug_info = [
            f"Player X: {int(player.rect.x)} Y: {int(player.rect.y)}",
            f"Enemy X: {int(enemy.rect.x)} Y: {int(enemy.rect.y)}",
            f"Distance: {int(player.rect.x - enemy.rect.x)}",
            f"Player Speed: {player.current_speed:.2f}",
            f"Enemy Speed: {enemy.speed:.2f}"
        ]
        
        y_offset = self.settings.screen_height - 110
        for info in debug_info:
            debug_text = debug_font.render(info, True, (255, 255, 255))
            debug_bg = debug_font.render(info, True, (0, 0, 0))
            screen.blit(debug_bg, (11, y_offset + 1))
            screen.blit(debug_text, (10, y_offset))
            y_offset += 20
