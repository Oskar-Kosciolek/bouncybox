from dataclasses import dataclass, field

@dataclass
class Config:
    # Prędkość
    initial_speed_x: float = 200.0
    initial_speed_y: float = -150.0

    # Grawitacja
    gravity_enabled: bool = False
    gravity_strength: float = 400.0   # px/s²

    # Piłeczka
    ball_radius: int = 10

    # Pudełko
    box_margin: int = 40

    # Fizyka odbicia
    restitution: float = 1.0  # 1.0 = idealne odbicie, 0.5 = traci połowę energii

    # System pudełek
    shrink_step: int = 15
    wall_anim_speed: float = 300.0