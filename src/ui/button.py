import pygame

class Button:
    """Clase para botones interactivos del menú"""
    def __init__(self, x, y, width, height, text, 
                 color=(100, 100, 100), 
                 hover_color=(150, 150, 150), 
                 text_color=(255, 255, 255),
                 font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        self.is_clicked = False
        
    def update(self, mouse_pos):
        """Actualiza el estado del botón según la posición del mouse"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def handle_event(self, event):
        """
        Maneja eventos del botón
        Retorna True si el botón fue clickeado
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_clicked = False
        
        return False
    
    def draw(self, screen):
        """Dibuja el botón en pantalla"""
        # Color basado en hover
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Dibujar botón con borde redondeado
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        
        # Dibujar borde
        border_color = (255, 255, 255) if self.is_hovered else (0, 0, 0)
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=10)
        
        # Dibujar texto centrado
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
