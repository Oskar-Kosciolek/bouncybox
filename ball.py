import pygame
from config import Config


class Ball:
    def __init__(self, x: float, y: float, config: Config):
        self.config = config
        self.x = x
        self.y = y
        self.vx: float = config.initial_speed_x
        self.vy: float = config.initial_speed_y

    @property
    def radius(self) -> int:
        return self.config.ball_radius

    @property
    def color(self):
        return (230, 80, 80)

    def update(self, dt: float) -> None:
        # Grawitacja — dodaje przyspieszenie do prędkości pionowej
        if self.config.gravity_enabled:
            self.vy += self.config.gravity_strength * dt

        self.x += self.vx * dt
        self.y += self.vy * dt

    def bounce(self, side: str) -> None:
        """Odbicie od ściany pudełka — odwraca odpowiedni składnik prędkości."""
        if side in ("left", "right"):
            self.vx *= -self.config.restitution
        elif side in ("top", "bottom"):
            self.vy *= -self.config.restitution

    def reset(self, box_rect: pygame.Rect) -> None:
        """Resetuje pozycję i prędkość po zmianie ustawień."""
        self.x = box_rect.centerx
        self.y = box_rect.centery
        self.vx = self.config.initial_speed_x
        self.vy = self.config.initial_speed_y

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
