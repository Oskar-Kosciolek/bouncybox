import pygame
from ball import Ball
from config import Config
from settings_panel import SettingsPanel

WINDOW_SIZE = (480, 480)
FPS = 60
BG_COLOR = (18, 18, 24)
BOX_COLOR = (60, 80, 120)


def make_box_rect(config: Config) -> pygame.Rect:
    m = config.box_margin
    return pygame.Rect(m, m, WINDOW_SIZE[0] - m * 2, WINDOW_SIZE[1] - m * 2)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("bouncybox")
    clock = pygame.time.Clock()

    config = Config()
    panel = SettingsPanel(config, window_height=WINDOW_SIZE[1])
    panel_offset_x = WINDOW_SIZE[0] - SettingsPanel.PANEL_WIDTH

    box_rect = make_box_rect(config)
    ball = Ball(box_rect.centerx, box_rect.centery, config)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_m:
                    panel.toggle()
                if event.key == pygame.K_r:
                    box_rect = make_box_rect(config)
                    ball.reset(box_rect)

            panel.handle_event(event, offset_x=panel_offset_x)

        ball.update(dt, box_rect)

        # Rysowanie
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, BOX_COLOR, box_rect, width=2)
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