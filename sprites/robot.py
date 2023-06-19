from arcade.resources import image_robot_idle
from sprites.enemy import Enemy

class Robot(Enemy):
    resource = image_robot_idle
    attack_cooldown = 3
    attack_damage = 10
    speed = 2.5
    charge_speed = 3
    max_health = 150
    def __init__(self, bar_list):
        super().__init__(self.resource, bar_list)
