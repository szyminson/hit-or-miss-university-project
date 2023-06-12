from sprites.killable_sprite import KillableSprite
from arcade.resources import image_female_person_idle, image_female_person_fall
from config import SPRITE_SIZE

class Player(KillableSprite):
       resource = image_female_person_idle
       def __init__(self, bar_list):
              super().__init__(self.resource, bar_list)
              self.center_x = SPRITE_SIZE * 5
              self.center_y = SPRITE_SIZE * 1
