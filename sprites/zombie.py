from arcade.resources import image_zombie_idle
from sprites.enemy import Enemy

class Zombie(Enemy):
    resource = image_zombie_idle
    def __init__(self, bar_list):
        super().__init__(self.resource, bar_list)
