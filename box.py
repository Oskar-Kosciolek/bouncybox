import pygame
from config import Config
from typing import TypedDict


class Wall(TypedDict):
    side: str
    alive: bool
    alpha: int
    rect: pygame.Rect
    target: pygame.Rect


class Box:
    THICKNESS = 4

    def __init__(self, margin: int, window_size: tuple, config: Config):
        self.config = config
        w, h = window_size
        t = self.THICKNESS

        # Docelowy prostokąt wewnętrzny pudełka
        self._target_rect = pygame.Rect(margin, margin, w - margin * 2, h - margin * 2)
        tr = self._target_rect

        # Każda ściana startuje poza oknem i wjeżdża do swojej pozycji w target_rect
        self.walls: list[Wall] = [
            {
                "side": "top",
                "alive": True,
                "alpha": 255,
                "rect": pygame.Rect(tr.left, -t, tr.width, t),
                "target": pygame.Rect(tr.left, tr.top, tr.width, t),
            },
            {
                "side": "bottom",
                "alive": True,
                "alpha": 255,
                "rect": pygame.Rect(tr.left, h, tr.width, t),
                "target": pygame.Rect(tr.left, tr.bottom - t, tr.width, t),
            },
            {
                "side": "left",
                "alive": True,
                "alpha": 255,
                "rect": pygame.Rect(-t, tr.top, t, tr.height),
                "target": pygame.Rect(tr.left, tr.top, t, tr.height),
            },
            {
                "side": "right",
                "alive": True,
                "alpha": 255,
                "rect": pygame.Rect(w, tr.top, t, tr.height),
                "target": pygame.Rect(tr.right - t, tr.top, t, tr.height),
            },
        ]

    @property
    def target_rect(self) -> pygame.Rect:
        return self._target_rect

    def update(self, dt: float) -> None:
        speed = self.config.wall_anim_speed
        for wall in self.walls:
            if wall["alive"]:
                rect = wall["rect"]
                target = wall["target"]
                if rect != target:
                    # Przesuń w stronę target z prędkością speed px/s — osobno x i y
                    step = speed * dt
                    dx = target.x - rect.x
                    dy = target.y - rect.y
                    if dx != 0:
                        move = int(min(abs(dx), step)) * (1 if dx > 0 else -1)
                        rect.x += move
                        if (dx > 0 and rect.x > target.x) or (dx < 0 and rect.x < target.x):
                            rect.x = target.x
                    if dy != 0:
                        move = int(min(abs(dy), step)) * (1 if dy > 0 else -1)
                        rect.y += move
                        if (dy > 0 and rect.y > target.y) or (dy < 0 and rect.y < target.y):
                            rect.y = target.y
            else:
                # Zanikanie po wybiciu
                if wall["alpha"] > 0:
                    wall["alpha"] = max(0, wall["alpha"] - int(400 * dt))

    def is_ready(self) -> bool:
        """Zwraca True jeśli wszystkie alive ściany dotarły do docelowej pozycji."""
        return all(
            wall["rect"] == wall["target"]
            for wall in self.walls
            if wall["alive"]
        )

    def check_collision(self, ball) -> str | None:
        """Sprawdza kolizję piłki z alive ścianami które dotarły do target.
        Zwraca nazwę strony lub None."""
        for wall in self.walls:
            if not wall["alive"] or wall["rect"] != wall["target"]:
                continue
            rect = wall["rect"]
            side = wall["side"]
            if side == "top":
                if ball.y - ball.radius <= rect.bottom and rect.left <= ball.x <= rect.right:
                    return "top"
            elif side == "bottom":
                if ball.y + ball.radius >= rect.top and rect.left <= ball.x <= rect.right:
                    return "bottom"
            elif side == "left":
                if ball.x - ball.radius <= rect.right and rect.top <= ball.y <= rect.bottom:
                    return "left"
            elif side == "right":
                if ball.x + ball.radius >= rect.left and rect.top <= ball.y <= rect.bottom:
                    return "right"
        return None

    def hit_wall(self, side: str) -> None:
        """Wybija daną ścianę — ustawia alive=False."""
        for wall in self.walls:
            if wall["side"] == side:
                wall["alive"] = False
                break

    def all_dead(self) -> bool:
        """Zwraca True jeśli wszystkie ściany są martwe."""
        return all(not wall["alive"] for wall in self.walls)

    def draw(self, surface: pygame.Surface) -> None:
        color = (60, 80, 120)
        for wall in self.walls:
            if wall["alive"]:
                pygame.draw.rect(surface, color, wall["rect"])
            elif wall["alpha"] > 0:
                # Fade out — ściana zanika po wybiciu
                s = pygame.Surface((wall["rect"].width, wall["rect"].height), pygame.SRCALPHA)
                s.fill((*color, wall["alpha"]))
                surface.blit(s, wall["rect"].topleft)
