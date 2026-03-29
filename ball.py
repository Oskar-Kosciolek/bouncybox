import pygame

class Ball:
    def __init__(self, x: float, y: float, radius: int = 10):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx: float = 200.0  # prędkość pozioma (px/s)
        self.vy: float = -150.0  # prędkość pionowa (px/s, ujemna = w górę)
        self.color = (230, 80, 80)

    def update(self, dt: float, box_rect: pygame.Rect) -> None:
        # Przesunięcie = prędkość × czas od ostatniej klatki
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Odbicie od lewej i prawej ściany
        if self.x - self.radius < box_rect.left:
            self.x = box_rect.left + self.radius
            self.vx *= -1

        if self.x + self.radius > box_rect.right:
            self.x = box_rect.right - self.radius
            self.vx *= -1

        # Odbicie od górnej i dolnej ściany
        if self.y - self.radius < box_rect.top:
            self.y = box_rect.top + self.radius
            self.vy *= -1

        if self.y + self.radius > box_rect.bottom:
            self.y = box_rect.bottom - self.radius
            self.vy *= -1

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)