from dataclasses import dataclass


@dataclass
class Config:
    # Prędkość startowa piłki
    initial_speed_x: float = 200.0
    initial_speed_y: float = -150.0

    # Grawitacja
    gravity_enabled: bool = False
    gravity_strength: float = 400.0   # px/s²

    # Piłeczka
    ball_radius: int = 10

    # Fizyka odbicia
    restitution: float = 1.0  # 1.0 = idealne, <1.0 = traci energię

    # Okręgi
    ring_spawn_interval: float = 3.0   # sekundy między nowymi okręgami
    ring_shrink_speed: float = 30.0    # px/s — prędkość zmniejszania się
    ring_start_radius: float = 220.0   # promień startowy
    ring_min_radius: float = 30.0      # minimalna wielkość

    # Dziury
    hole_count: int = 1                # liczba dziur na okręgu (1-4)
    hole_size: float = 45.0            # rozmiar dziury w stopniach
    hole_moving: bool = False          # czy dziura się porusza
    hole_move_speed: float = 60.0      # deg/s — prędkość ruchu dziury
