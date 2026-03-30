import pygame

class SettingsPanel:
    PANEL_WIDTH = 280
    PANEL_HEIGHT = 480
    BG_COLOR = (24, 24, 32)
    TEXT_COLOR = (200, 200, 220)
    ACCENT_COLOR = (100, 140, 220)
    SLIDER_BG = (50, 50, 65)
    SLIDER_FG = (100, 140, 220)
    FONT_SIZE = 15

    def __init__(self, config):
        self.config = config
        self.screen = None
        self.font = None
        self.active = False
        self._dragging = None  # który slider jest aktywnie przeciągany

        # Definicja suwaków: (etykieta, atrybut w config, min, max, czy float)
        self.sliders = [
            ("Prędkość X (px/s)",    "initial_speed_x",    50,   600,  True),
            ("Prędkość Y (px/s)",    "initial_speed_y",   -600, -50,   True),
            ("Siła grawitacji",      "gravity_strength",   50,   1200, True),
            ("Rozmiar piłki",        "ball_radius",        5,    40,   False),
            ("Margines pudełka",     "box_margin",         10,   120,  False),
            ("Restytucja (odbicie)", "restitution",        0.3,  1.0,  True),
        ]

    def open(self):
        if self.active:
            return
        self.active = True
        self.screen = pygame.display.set_mode(
            (SettingsPanel.PANEL_WIDTH, SettingsPanel.PANEL_HEIGHT),
            flags=0,
            display=0,
        )
        # Nowe okno zastępuje główne w jednookienkowym Pygame —
        # dlatego zaraz zobaczymy jak to obejść przez SDL
        pygame.display.set_caption("bouncybox — settings")
        self.font = pygame.font.SysFont("segoeui", self.FONT_SIZE)

    def close(self):
        self.active = False

    def handle_event(self, event) -> bool:
        """Zwraca True jeśli event został skonsumowany przez panel."""
        if not self.active:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (_, attr, min_val, max_val, _) in enumerate(self.sliders):
                track_rect = self._track_rect(i)
                if track_rect.collidepoint(event.pos):
                    self._dragging = i
                    self._update_slider(i, event.pos[0])
                    return True

            # Toggle grawitacji
            toggle_rect = self._toggle_rect()
            if toggle_rect.collidepoint(event.pos):
                self.config.gravity_enabled = not self.config.gravity_enabled
                return True

        if event.type == pygame.MOUSEBUTTONUP:
            self._dragging = None

        if event.type == pygame.MOUSEMOTION and self._dragging is not None:
            self._update_slider(self._dragging, event.pos[0])
            return True

        return False

    def draw(self):
        if not self.active or self.screen is None:
            return
        self.screen.fill(self.BG_COLOR)
        self._draw_title()
        self._draw_gravity_toggle()
        for i in range(len(self.sliders)):
            self._draw_slider(i)
        pygame.display.flip()

    # --- Prywatne metody rysujące ---

    def _draw_title(self):
        title = self.font.render("⚙ Ustawienia", True, self.TEXT_COLOR)
        self.screen.blit(title, (20, 16))

    def _draw_gravity_toggle(self):
        toggle_rect = self._toggle_rect()
        color = self.ACCENT_COLOR if self.config.gravity_enabled else self.SLIDER_BG
        pygame.draw.rect(self.screen, color, toggle_rect, border_radius=4)
        label = self.font.render(
            f"Grawitacja: {'ON' if self.config.gravity_enabled else 'OFF'}",
            True, self.TEXT_COLOR
        )
        self.screen.blit(label, (20, toggle_rect.y - 20))

    def _draw_slider(self, index: int):
        label, attr, min_val, max_val, is_float = self.sliders[index]
        value = getattr(self.config, attr)

        y = self._slider_y(index)
        track = self._track_rect(index)

        # Etykieta + wartość
        text = self.font.render(f"{label}: {value:.1f}" if is_float else f"{label}: {value}", True, self.TEXT_COLOR)
        self.screen.blit(text, (20, y))

        # Track (tło suwaka)
        pygame.draw.rect(self.screen, self.SLIDER_BG, track, border_radius=4)

        # Fill (wypełnienie do aktualnej wartości)
        fill_w = int((value - min_val) / (max_val - min_val) * track.width)
        fill_rect = pygame.Rect(track.x, track.y, fill_w, track.height)
        pygame.draw.rect(self.screen, self.SLIDER_FG, fill_rect, border_radius=4)

        # Uchwyt
        handle_x = track.x + fill_w
        pygame.draw.circle(self.screen, (200, 220, 255), (handle_x, track.centery), 7)

    def _update_slider(self, index: int, mouse_x: int):
        _, attr, min_val, max_val, is_float = self.sliders[index]
        track = self._track_rect(index)
        ratio = max(0.0, min(1.0, (mouse_x - track.x) / track.width))
        raw = min_val + ratio * (max_val - min_val)
        setattr(self.config, attr, float(raw) if is_float else int(raw))

    def _slider_y(self, index: int) -> int:
        # Pierwszy slider zaczyna się pod togglem grawitacji
        return 110 + index * 55

    def _track_rect(self, index: int) -> pygame.Rect:
        y = self._slider_y(index)
        return pygame.Rect(20, y + 22, self.PANEL_WIDTH - 40, 8)

    def _toggle_rect(self) -> pygame.Rect:
        return pygame.Rect(20, 62, self.PANEL_WIDTH - 40, 28)