from src.models.character import Character

from src.models.character import Character

class TankCharacter(Character):
    def __init__(
        self,
        name: str,
        health: int = 100,
        reduction_percent: float = 0.30,
        flat_reduction: int = 0
    ):
        super().__init__(name=name, health=health)
        self.reduction_percent = max(0.0, min(1.0, float(reduction_percent)))
        self.flat_reduction = max(0, int(flat_reduction))

    def percent_reduced(self, damage: int) -> int:
        dmg = max(0, int(damage))
        return int(round(dmg * (1.0 - self.reduction_percent)))

    def flat_reduced(self, damage_after_percent: int) -> int:
        return max(0, int(damage_after_percent) - self.flat_reduction)

    def compute_reduced_damage(self, damage: int) -> int:
        after_percent = self.percent_reduced(damage)
        after_flat = self.flat_reduced(after_percent)
        return after_flat

    def take_damage(self, damage: int) -> None:
        if not self.is_alive:
            return
        final_damage = self.compute_reduced_damage(damage)
        super().take_damage(final_damage)
