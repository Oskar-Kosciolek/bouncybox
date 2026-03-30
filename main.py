import pygame
from ball import Ball
from box import Box
from config import Config
from particles import ParticleSystem
from settings_panel import SettingsPanel

WINDOW_SIZE = (480, 480)
FPS = 60
BG_COLOR = (18, 18, 24)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("bouncybox")
    clock = pygame.time.Clock()

    config = Config()
    panel = SettingsPanel(config, window_height=WINDOW_SIZE[1])
    panel_offset_x = WINDOW_SIZE[0] - SettingsPanel.PANEL_WIDTH

    current_margin = config.box_margin
    boxes: list[Box] = [Box(current_margin, WINDOW_SIZE, config)]
    particles = ParticleSystem()
    spawn_timer: float = 0.0
    ball = Ball(boxes[0].rect.centerx, boxes[0].rect.centery, config)

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
                    panel.toggle()
                if event.key == pygame.K_r:
                    current_margin = config.box_margin
                    boxes = [Box(current_margin, WINDOW_SIZE, config)]
                    particles = ParticleSystem()
                    spawn_timer = 0.0
                    ball.reset(boxes[0].rect)

            panel.handle_event(event, offset_x=panel_offset_x)

        # --- Logika ---
        ball.update(dt)

        for box in boxes:
            box.update(dt)

        # Timer spawnu — niezależny od kolizji
        spawn_timer += dt
        if spawn_timer >= config.box_spawn_interval:
            current_margin += config.shrink_step
            min_playable = ball.radius * 6
            if WINDOW_SIZE[0] - current_margin * 2 > min_playable:
                boxes.append(Box(current_margin, WINDOW_SIZE, config))
            spawn_timer = 0.0

        # Kolizja tylko z ostatnim (najmłodszym, najbliższym środka) pudełkiem
        if boxes:
            active_box = boxes[-1]
            side = active_box.check_collision(ball)
            if side is not None:
                ball.bounce(side)
                # Korekta pozycji piłki żeby nie wchodziła w ścianę
                if side == "left":
                    ball.x = active_box.rect.left + 6 + ball.radius
                elif side == "right":
                    ball.x = active_box.rect.right - 6 - ball.radius
                elif side == "top":
                    ball.y = active_box.rect.top + 6 + ball.radius
                elif side == "bottom":
                    ball.y = active_box.rect.bottom - 6 - ball.radius
                # Zniszcz pudełko i emituj cząsteczki
                particles.explode(active_box.rect, active_box.color)
                active_box.alive = False
                boxes.remove(active_box)

        particles.update(dt)

        # --- Rysowanie ---
        screen.fill(BG_COLOR)

        for box in boxes:
            box.draw(screen)

        particles.draw(screen)
        ball.draw(screen)

        # Hint — tylko gdy panel zamknięty
        if not panel.active:
            font = pygame.font.SysFont("segoeui", 13)
            hint = font.render("M — ustawienia", True, (70, 70, 90))
            screen.blit(hint, (10, WINDOW_SIZE[1] - 18))

        # Panel na wierzchu
        panel.draw(screen, offset_x=panel_offset_x)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
