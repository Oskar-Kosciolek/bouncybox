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

    def __init__(self, config: Config):
        self.config = config
        self.active = False
        self._dragging = None
        self._font = None

        # (etykieta, atrybut, min, max, is_float)
        self.sliders = [
            ("Prędkość X",              "initial_speed_x",      50,   600,  True),
            ("Prędkość Y",              "initial_speed_y",     -600,  -50,  True),
            ("Siła grawitacji",         "gravity_strength",      50,  1200,  True),
            ("Restytucja",              "restitution",          0.3,   1.0,  True),
            ("Odstęp okręgów (s)",      "ring_spawn_interval",  0.5,  10.0,  True),
            ("Prędkość zwężania",       "ring_shrink_speed",     10,   150,  True),
            ("Promień startowy",        "ring_start_radius",    100,   230,  True),
            ("Liczba dziur",            "hole_count",             1,     4,  False),
            ("Rozmiar dziury (deg)",    "hole_size",             15,   120,  True),
            ("Prędkość dziury",         "hole_move_speed",       10,   180,  True),
        ]

    def toggle(self):
        self.active = not self.active

    def _get_font(self) -> pygame.font.Font:
        # Inicjalizacja leniwa — font musi być tworzony po pygame.init()
        if self._font is None:
            self._font = pygame.font.SysFont("segoeui", self.FONT_SIZE)
        return self._font

    def handle_event(self, event, offset_x: int = 0, window_h: int = 480) -> bool:
        """
        offset_x: x początku panelu w przestrzeni okna.
        Zwraca True jeśli event skonsumowany.
        """
        if not self.active:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            local_x = event.pos[0] - offset_x
            local_y = event.pos[1]

            # Toggle grawitacji
            if self._toggle_gravity_rect().collidepoint(local_x, local_y):
                self.config.gravity_enabled = not self.config.gravity_enabled
                return True

            # Toggle ruchomej dziury
            if self._toggle_hole_rect().collidepoint(local_x, local_y):
                self.config.hole_moving = not self.config.hole_moving
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

    def draw(self, screen: pygame.Surface, offset_x: int = 0, window_h: int = 480):
        if not self.active:
            return

        font = self._get_font()

        # Surface z alpha — przezroczystość tła panelu
        panel = pygame.Surface((self.PANEL_WIDTH, window_h), pygame.SRCALPHA)
        panel.fill(self.BG_COLOR)

        # Tytuł
        title = font.render("Ustawienia", True, self.TEXT_COLOR)
        panel.blit(title, (16, 14))

        hint = font.render("R — reset   ESC — wyjście", True, self.LABEL_COLOR)
        panel.blit(hint, (16, 30))

        # Toggle grawitacji
        self._draw_toggle(panel, font, self._toggle_gravity_rect(),
                          self.config.gravity_enabled, "Grawitacja")

        # Toggle ruchomej dziury
        self._draw_toggle(panel, font, self._toggle_hole_rect(),
                          self.config.hole_moving, "Ruchoma dziura")

        # Suwaki
        for i in range(len(self.sliders)):
            self._draw_slider(panel, font, i)

        screen.blit(panel, (offset_x, 0))

        # Linia oddzielająca panel od gry
        pygame.draw.line(screen, (60, 60, 90),
                         (offset_x, 0), (offset_x, window_h), 1)

    # --- Geometria (współrzędne lokalne wewnątrz panelu) ---

    def _toggle_gravity_rect(self) -> "pygame.Rect":
        return pygame.Rect(16, 54, self.PANEL_WIDTH - 32, 22)  # type: ignore[return-value]

    def _toggle_hole_rect(self) -> "pygame.Rect":
        return pygame.Rect(16, 82, self.PANEL_WIDTH - 32, 22)  # type: ignore[return-value]

    def _slider_y(self, index: int) -> int:
        return 118 + index * 50

    def _track_rect(self, index: int) -> "pygame.Rect":
        return pygame.Rect(16, self._slider_y(index) + 18, self.PANEL_WIDTH - 32, 6)  # type: ignore[return-value]

    # --- Rysowanie elementów ---

    def _draw_toggle(self, surface: pygame.Surface, font: pygame.font.Font,
                     rect: pygame.Rect, state: bool, label: str) -> None:
        color = self.ACCENT_COLOR if state else self.SLIDER_BG
        pygame.draw.rect(surface, color, rect, border_radius=4)
        text = font.render(f"{label}: {'ON' if state else 'OFF'}", True, self.TEXT_COLOR)
        surface.blit(text, (rect.x + 8, rect.y + 4))

    def _draw_slider(self, surface: pygame.Surface, font: pygame.font.Font,
                     index: int) -> None:
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

    def _update_value(self, index: int, local_x: int) -> None:
        _, attr, min_val, max_val, is_float = self.sliders[index]
        track = self._track_rect(index)
        ratio = max(0.0, min(1.0, (local_x - track.x) / track.width))
        raw = min_val + ratio * (max_val - min_val)
        setattr(self.config, attr, float(raw) if is_float else int(raw))
