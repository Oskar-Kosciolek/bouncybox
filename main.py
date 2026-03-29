import pygame
from ball import Ball

# --- Stałe ---
WINDOW_SIZE = (480, 480)
BOX_MARGIN = 40
FPS = 60
BG_COLOR = (18, 18, 24)
BOX_COLOR = (60, 80, 120)

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("bouncybox")
    clock = pygame.time.Clock()

    # Pudełko — pygame.Rect(x, y, width, height)
    box_rect = pygame.Rect(
        BOX_MARGIN,
        BOX_MARGIN,
        WINDOW_SIZE[0] - BOX_MARGIN * 2,
        WINDOW_SIZE[1] - BOX_MARGIN * 2,
    )

    # Piłeczka startuje na środku pudełka
    ball = Ball(box_rect.centerx, box_rect.centery)

    # --- Game loop ---
    running = True
    while running:
        # dt w sekundach — Clock.tick() zwraca milisekundy
        dt = clock.tick(FPS) / 1000.0

        # 1. Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # 2. Logika
        ball.update(dt, box_rect)

        # 3. Rysowanie
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, BOX_COLOR, box_rect, width=2)  # width=2 = tylko ramka
        ball.draw(screen)

        pygame.display.flip()  # pokaż wyrenderowaną klatkę

    pygame.quit()

if __name__ == "__main__":
    main()