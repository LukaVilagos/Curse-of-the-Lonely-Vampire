from classes.Effect import Effect
from classes.Effect import EffectTypes

class SlowEffect(Effect):
    def __init__(self):
        super().__init__("Slow", "The target is slowed down", 30, EffectTypes.SLOW)

    def effect(self, target):
        setattr(target, 'speed', target.speed ** 0.7)