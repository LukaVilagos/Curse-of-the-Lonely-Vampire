from utils.pg import pg

class NPC:
    def __init__(self, image, name: str, description: str, location, dialogue: [], scale):
        witdth = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(witdth * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.location = location
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.dialogue_step = -1
        
    def interact(self):
        self.dialogue_step += 1
        self.dialogue.visible = True
        
        