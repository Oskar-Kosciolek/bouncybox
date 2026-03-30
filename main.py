import pygame
from ball import Ball
from box import Box
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

    config = Config()
    panel = SettingsPanel(config, window_height=WINDOW_SIZE[1])
    panel_offset_x = WINDOW_SIZE[0] - SettingsPanel.PANEL_WIDTH

    current_margin = config.box_margin
    boxes: list[Box] = [Box(current_margin, WINDOW_SIZE, config)]
    ball = Ball(boxes[0].target_rect.centerx, boxes[0].target_rect.centery, config)

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
                    ball.reset(boxes[0].target_rect)

            panel.handle_event(event, offset_x=panel_offset_x)

        # --- Logika ---
        ball.update(dt)

        for box in boxes:
            box.update(dt)

        # Kolizja tylko z aktywnym (pierwszym) pudełkiem
        if boxes:
            active_box = boxes[0]
            if active_box.is_ready():
                side = active_box.check_collision(ball)
                if side is not None:
                    active_box.hit_wall(side)
                    ball.bounce(side)

                    # Korekta pozycji piłki żeby nie wchodziła w ścianę
                    t = active_box.target_rect
                    tk = Box.THICKNESS
                    if side == "top":
                        ball.y = t.top + tk + ball.radius
                    elif side == "bottom":
                        ball.y = t.bottom - tk - ball.radius
                    elif side == "left":
                        ball.x = t.left + tk + ball.radius
                    elif side == "right":
                        ball.x = t.right - tk - ball.radius

                    # Nowe pudełko po wybiciu wszystkich ścian
                    if active_box.all_dead():
                        current_margin += config.shrink_step
                        min_size = ball.radius * 4
                        if WINDOW_SIZE[0] - current_margin * 2 > min_size:
                            boxes.append(Box(current_margin, WINDOW_SIZE, config))

        # Usuń w pełni zanikłe martwe pudełka
        boxes = [
            b for b in boxes
            if not (b.all_dead() and all(w["alpha"] == 0 for w in b.walls))
        ]

        # --- Rysowanie ---
        screen.fill(BG_COLOR)

        for box in boxes:
            box.draw(screen)

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
