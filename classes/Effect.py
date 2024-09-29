from enum import Enum

class EffectTypes(Enum):
    SLOW = "Slow"
    STUN = "Stun"

class Effect():
    def __init__(self, name, description, duration, type: EffectTypes):
        self.name = name
        self.description = description
        self.duration = duration
        self.type = type

    def __str__(self):
        return self.name
    
    def effect(self, target):
        print(self.description, target)

    def apply(self, target):
        self.effect(target)
