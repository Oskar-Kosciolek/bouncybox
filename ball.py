import pygame
from config import Config


class Ball:
    def __init__(self, x: float, y: float, config: Config) -> None:
        self.config = config
        self.x = x
        self.y = y
        self.vx = config.initial_speed_x
        self.vy = config.initial_speed_y
        self.radius = 8
        self.color = (230, 80, 80)
        self.collision_cooldown = 0.0  # czas blokady po ostatnim odbiciu

    def update(self, dt: float) -> None:
        # Grawitacja
        if self.config.gravity_enabled:
            self.vy += self.config.gravity_strength * dt

        self.collision_cooldown = max(0.0, self.collision_cooldown - dt)
        self.x += self.vx * dt
        self.y += self.vy * dt

    def bounce_radial(self, nx: float, ny: float) -> None:
        """Odbicie od normalnej (nx, ny) — wektor jednostkowy od środka okręgu do piłki."""
        dot = self.vx * nx + self.vy * ny
        self.vx = (self.vx - 2 * dot * nx) * self.config.restitution
        self.vy = (self.vy - 2 * dot * ny) * self.config.restitution
        self.collision_cooldown = 0.05

    def reset(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.vx = self.config.initial_speed_x
        self.vy = self.config.initial_speed_y
        self.collision_cooldown = 0.0

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
