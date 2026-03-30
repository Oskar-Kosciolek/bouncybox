import pygame
from config import Config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ball import Ball


class Box:
    def __init__(self, margin: int, window_size: tuple, config: Config):
        self.margin = margin
        self.window_size = window_size
        self.config = config
        self.alive = True
        w, h = window_size
        # Kwadrat pojawia się od razu w docelowej pozycji — bez animacji wjazdu
        self.rect = pygame.Rect(margin, margin, w - margin * 2, h - margin * 2)
        self.color = (60, 80, 120)

    def update(self, dt: float) -> None:
        pass

    def check_collision(self, ball: "Ball") -> str | None:
        """Sprawdza czy piłka dotyka ramki kwadratu (grubość kolizji = 6px).
        Zwraca stronę kolizji lub None."""
        if ball.y - ball.radius <= self.rect.top + 6:
            return "top"
        if ball.y + ball.radius >= self.rect.bottom - 6:
            return "bottom"
        if ball.x - ball.radius <= self.rect.left + 6:
            return "left"
        if ball.x + ball.radius >= self.rect.right - 6:
            return "right"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect, width=3)
