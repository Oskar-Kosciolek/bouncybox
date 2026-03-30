import pygame
from config import Config


class SettingsPanel:
    PANEL_WIDTH = 240
    BG_COLOR = (24, 24, 34, 220)       # RGBA — alpha 220/255
    TEXT_COLOR = (200, 200, 220)
    LABEL_COLOR = (120, 130, 160)
    ACCENT_COLOR = (100, 140, 220)
    SLIDER_BG = (45, 45, 60)
    SLIDER_FG = (100, 140, 220)
    FONT_SIZE = 13

    def __init__(self, config: Config, window_height: int):
        self.config = config
        self.window_height = window_height
        self.active = False
        self._dragging = None
        self._font = None

        # (etykieta, atrybut, min, max, is_float)
        self.sliders = [
            ("Prędkość X",      "initial_speed_x",   50,   600,  True),
            ("Prędkość Y",      "initial_speed_y",  -600,  -50,  True),
            ("Siła grawitacji", "gravity_strength",   50,  1200,  True),
            ("Rozmiar piłki",   "ball_radius",         5,    40,  False),
            ("Margines pudełka","box_margin",          10,   120,  False),
            ("Restytucja",      "restitution",        0.3,   1.0,  True),
            ("Odstęp kwadratów (s)", "box_spawn_interval", 0.5, 10.0, True),
        ]

    def toggle(self):
        self.active = not self.active

    def _get_font(self) -> pygame.font.Font:
        # Inicjalizacja leniwa — font musi być tworzony po pygame.init()
        if self._font is None:
            self._font = pygame.font.SysFont("segoeui", self.FONT_SIZE)
        return self._font

    def handle_event(self, event, offset_x: int) -> bool:
        """
        offset_x: x początku panelu w przestrzeni okna.
        Zwraca True jeśli event skonsumowany.
        """
        if not self.active:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Przeliczamy pozycję myszy na lokalną przestrzeń panelu
            local_x = event.pos[0] - offset_x
            local_y = event.pos[1]

            toggle_rect = self._toggle_rect()
            if toggle_rect.collidepoint(local_x, local_y):
                self.config.gravity_enabled = not self.config.gravity_enabled
                return True

            for i in range(len(self.sliders)):
                track = self._track_rect(i)
                if track.collidepoint(local_x, local_y):
                    self._dragging = i
                    self._update_value(i, local_x)
                    return True

        if event.type == pygame.MOUSEBUTTONUP:
            self._dragging = None

        if event.type == pygame.MOUSEMOTION and self._dragging is not None:
            local_x = event.pos[0] - offset_x
            self._update_value(self._dragging, local_x)
            return True

        return False

    def draw(self, screen: pygame.Surface, offset_x: int):
        if not self.active:
            return

        font = self._get_font()

        # Surface z alpha — to pozwala na przezroczystość
        panel = pygame.Surface((self.PANEL_WIDTH, self.window_height), pygame.SRCALPHA)
        panel.fill(self.BG_COLOR)

        # Tytuł
        title = font.render("⚙ Ustawienia", True, self.TEXT_COLOR)
        panel.blit(title, (16, 14))

        hint = font.render("R — reset piłki", True, self.LABEL_COLOR)
        panel.blit(hint, (16, 30))

        # Toggle grawitacji
        self._draw_toggle(panel, font)

        # Suwaki
        for i in range(len(self.sliders)):
            self._draw_slider(panel, font, i)

        screen.blit(panel, (offset_x, 0))

        # Linia oddzielająca panel od gry
        pygame.draw.line(screen, (60, 60, 90), (offset_x, 0), (offset_x, self.window_height), 1)

    # --- Geometria (współrzędne lokalne wewnątrz panelu) ---

    def _toggle_rect(self) -> pygame.Rect:
        return pygame.Rect(16, 58, self.PANEL_WIDTH - 32, 24)

    def _slider_y(self, index: int) -> int:
        return 100 + index * 52

    def _track_rect(self, index: int) -> pygame.Rect:
        return pygame.Rect(16, self._slider_y(index) + 20, self.PANEL_WIDTH - 32, 6)

    # --- Rysowanie elementów ---

    def _draw_toggle(self, surface: pygame.Surface, font: pygame.font.Font):
        rect = self._toggle_rect()
        color = self.ACCENT_COLOR if self.config.gravity_enabled else self.SLIDER_BG
        pygame.draw.rect(surface, color, rect, border_radius=4)
        label = font.render(
            f"Grawitacja: {'ON' if self.config.gravity_enabled else 'OFF'}",
            True, self.TEXT_COLOR
        )
        surface.blit(label, (rect.x + 8, rect.y + 5))

    def _draw_slider(self, surface: pygame.Surface, font: pygame.font.Font, index: int):
        label, attr, min_val, max_val, is_float = self.sliders[index]
        value = getattr(self.config, attr)
        y = self._slider_y(index)
        track = self._track_rect(index)

        # Etykieta z wartością
        val_str = f"{value:.1f}" if is_float else str(value)
        text = font.render(f"{label}: {val_str}", True, self.TEXT_COLOR)
        surface.blit(text, (16, y))

        # Track
        pygame.draw.rect(surface, self.SLIDER_BG, track, border_radius=3)

        # Fill
        ratio = (value - min_val) / (max_val - min_val)
        fill_w = max(0, int(ratio * track.width))
        if fill_w > 0:
            pygame.draw.rect(surface, self.SLIDER_FG,
                             pygame.Rect(track.x, track.y, fill_w, track.height),
                             border_radius=3)

        # Uchwyt
        handle_x = track.x + fill_w
        pygame.draw.circle(surface, (200, 220, 255), (handle_x, track.centery), 6)

    def _update_value(self, index: int, local_x: int):
        _, attr, min_val, max_val, is_float = self.sliders[index]
        track = self._track_rect(index)
        ratio = max(0.0, min(1.0, (local_x - track.x) / track.width))
        raw = min_val + ratio * (max_val - min_val)
        setattr(self.config, attr, float(raw) if is_float else int(raw))