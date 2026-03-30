import random
import math
import pygame


class Particle:
    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: tuple[int, int, int], lifetime: float):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.size = random.randint(2, 5)

    def update(self, dt: float) -> bool:
        """Aktualizuje pozycję i wiek. Zwraca True dopóki cząsteczka żyje."""
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        return self.age < self.lifetime

    def draw(self, surface: pygame.Surface) -> None:
        alpha = 1.0 - (self.age / self.lifetime)  # 1.0 → 0.0
        r, g, b = self.color
        faded: tuple[int, int, int] = (int(r * alpha), int(g * alpha), int(b * alpha))
        pygame.draw.circle(surface, faded, (int(self.x), int(self.y)), self.size)


class ParticleSystem:
    def __init__(self):
        self.particles: list[Particle] = []

    def explode(self, rect: pygame.Rect, color: tuple[int, int, int]) -> None:
        """Emituje 60 cząsteczek (15 na każdej krawędzi) po zniszczeniu kwadratu."""
        # Zbierz punkty na każdej krawędzi
        points: list[tuple[float, float]] = []
        for i in range(15):
            t = i / 14
            points.append((rect.left + t * rect.width, float(rect.top)))
            points.append((rect.left + t * rect.width, float(rect.bottom)))
            points.append((float(rect.left),  rect.top + t * rect.height))
            points.append((float(rect.right), rect.top + t * rect.height))

        cx, cy = rect.centerx, rect.centery
        for x, y in points:
            dx = x - cx
            dy = y - cy
            dist = max(math.sqrt(dx * dx + dy * dy), 1.0)
            speed = random.uniform(80, 250)
            vx = (dx / dist) * speed + random.uniform(-30, 30)
            vy = (dy / dist) * speed + random.uniform(-30, 30)
            # Losowa wariacja koloru ±30 per kanał
            r, g, b = color
            varied: tuple[int, int, int] = (
                max(0, min(255, r + random.randint(-30, 30))),
                max(0, min(255, g + random.randint(-30, 30))),
                max(0, min(255, b + random.randint(-30, 30))),
            )
            lifetime = random.uniform(0.4, 1.0)
            self.particles.append(Particle(x, y, vx, vy, varied, lifetime))

    def update(self, dt: float) -> None:
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            p.draw(surface)
