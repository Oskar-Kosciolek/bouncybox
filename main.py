import pygame
from ball import Ball
from circle_ring import CircleRing
from particles import ParticleSystem
from config import Config
from settings_panel import SettingsPanel

WINDOW_SIZE = (480, 480)
FPS = 60
BG_COLOR = (18, 18, 24)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("bouncybox")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 13)

    config = Config()
    panel = SettingsPanel(config, window_height=WINDOW_SIZE[1])
    cx, cy = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2

    particles = ParticleSystem()
    rings: list[CircleRing] = [CircleRing(config, WINDOW_SIZE)]
    ball = Ball(cx, cy, config)
    spawn_timer: float = 0.0
    game_won: bool = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Zdarzenia ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_m:
                    panel.active = not panel.active
                if event.key == pygame.K_r:
                    rings = [CircleRing(config, WINDOW_SIZE)]
                    particles = ParticleSystem()
                    spawn_timer = 0.0
                    game_won = False
                    ball.reset(cx, cy)
            panel.handle_event(event)

        # --- Logika ---
        if not game_won:
            ball.update(dt)

            margin = ball.radius
            if (ball.x < -margin or ball.x > WINDOW_SIZE[0] + margin or
                    ball.y < -margin or ball.y > WINDOW_SIZE[1] + margin):
                game_won = True

            # Spawn nowych okręgów co ring_spawn_interval sekund
            spawn_timer += dt
            if spawn_timer >= config.ring_spawn_interval:
                new_ring = CircleRing(config, WINDOW_SIZE)
                alive_radii = [r.radius for r in rings if r.alive]
                if alive_radii:
                    smallest = min(alive_radii)
                    new_ring.min_radius = max(smallest - 35, ball.radius * 3)
                rings.append(new_ring)
                spawn_timer = 0.0

            # Aktualizuj okręgi
            for ring in rings:
                ring.update(dt)

            # Kolizje — sprawdzaj WSZYSTKIE żywe okręgi
            for ring in reversed(rings):
                if ring.alive:
                    was_alive = ring.alive
                    collided = ring.check_collision(ball)
                    if was_alive and not ring.alive and not ring.exploded:
                        particles.explode_ring(ring.cx, ring.cy, ring.radius, ring.color)
                        ring.exploded = True
                    if collided:
                        break  # przerwij po pierwszym odbiciu, ale nie po zniszczeniu

            # Usuń okręgi całkowicie przezroczyste
            rings = [r for r in rings if not r.is_faded()]

        particles.update(dt)

        # --- Rysowanie ---
        screen.fill(BG_COLOR)
        for ring in rings:
            ring.draw(screen)
        particles.draw(screen)
        ball.draw(screen)

        if game_won:
            win_font = pygame.font.SysFont("segoeui", 64, bold=True)
            win_text = win_font.render("Win!", True, (255, 220, 80))
            rect = win_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            screen.blit(win_text, rect)
            sub_font = pygame.font.SysFont("segoeui", 18)
            sub = sub_font.render("Naciśnij R aby zagrać ponownie", True, (180, 180, 200))
            sub_rect = sub.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 60))
            screen.blit(sub, sub_rect)

        hint = font.render("M — ustawienia   R — reset", True, (80, 80, 100))
        screen.blit(hint, (10, WINDOW_SIZE[1] - 20))

        if panel.active:
            panel.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
