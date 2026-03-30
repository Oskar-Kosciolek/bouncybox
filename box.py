import pygame
from config import Config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ball import Ball

_COLLISION_THICKNESS = 6
_START_MARGIN = 4


class Box:
    def __init__(self, target_margin: int, window_size: tuple, config: Config):
        self.target_margin = target_margin
        self.window_size = window_size
        self.config = config
        self.alive = True
        self.arrived = False
        self.color = (60, 80, 120)
        w, h = window_size

        # Docelowy prostokąt — coraz ciasniejszy
        self.target_rect = pygame.Rect(
            target_margin, target_margin,
            w - target_margin * 2, h - target_margin * 2,
        )

        # Startowy prostokąt — prawie cały ekran
        self.rect = pygame.Rect(
            _START_MARGIN, _START_MARGIN,
            w - _START_MARGIN * 2, h - _START_MARGIN * 2,
        )

        # Floaty do płynnej animacji (pygame.Rect przechowuje tylko int)
        self._left: float = float(_START_MARGIN)
        self._right: float = float(w - _START_MARGIN)
        self._top: float = float(_START_MARGIN)
        self._bottom: float = float(h - _START_MARGIN)

    def update(self, dt: float) -> None:
        if self.arrived:
            return

        speed = self.config.wall_anim_speed * dt
        tl, tr, tt, tb = (float(self.target_rect.left), float(self.target_rect.right),
                          float(self.target_rect.top),  float(self.target_rect.bottom))

        # Każda krawędź przesuwa się niezależnie w stronę target
        if self._left < tl:
            self._left = min(self._left + speed, tl)
        if self._right > tr:
            self._right = max(self._right - speed, tr)
        if self._top < tt:
            self._top = min(self._top + speed, tt)
        if self._bottom > tb:
            self._bottom = max(self._bottom - speed, tb)

        # Zastosuj float → int do pygame.Rect
        self.rect.left = int(self._left)
        self.rect.top = int(self._top)
        self.rect.width = int(self._right - self._left)
        self.rect.height = int(self._bottom - self._top)

        if self.rect == self.target_rect:
            self.arrived = True

    def check_collision(self, ball: "Ball") -> str | None:
        """Sprawdza czy piłka dotyka ramki kwadratu (grubość kolizji = 6px).
        Zwraca stronę kolizji lub None."""
        t = _COLLISION_THICKNESS
        if ball.y - ball.radius <= self.rect.top + t:
            return "top"
        if ball.y + ball.radius >= self.rect.bottom - t:
            return "bottom"
        if ball.x - ball.radius <= self.rect.left + t:
            return "left"
        if ball.x + ball.radius >= self.rect.right - t:
            return "right"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect, width=3)
