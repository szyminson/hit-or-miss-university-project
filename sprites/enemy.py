from enum import Enum
from math import cos, sin, sqrt, atan2
from uuid import uuid4
from random import randint
from sprites.killable_sprite import KillableSprite

class BehaviourMode(Enum):
    ATTACK = 1
    PANIC = 2
    REST = 3

class Enemy(KillableSprite):
    attack_cooldown = 1
    attack_damage = 2
    speed = 2
    charge_speed = 4
    """
    This class represents the Enemy on our screen.
    """
    def __init__(self, resource, bar_list):
        super().__init__(resource, bar_list)
        self.position_list = [[self.center_x, self.center_y]]
        self.cur_position = 0
        self.cur_speed = self.speed
        self.cur_mode = BehaviourMode.REST
        self.guid = uuid4()
        self.player_offset = randint(-12, 12)
        self.current_attack_cooldown = 0

    def next_position(self):
        """ Have the sprite follow a path """
        
        # Where are we
        start_x = self.center_x
        start_y = self.center_y
        # Where are we going
        if not self.position_list or len(self.position_list) <= self.cur_position:
            return
        dest_x = self.position_list[self.cur_position][0]
        dest_y = self.position_list[self.cur_position][1]

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = atan2(y_diff, x_diff)

        # How far are we?
        distance = sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(self.cur_speed, distance)

        # Calculate vector to travel
        change_x = cos(angle) * speed
        change_y = sin(angle) * speed
        # Update our location
        self.center_x += change_x
        self.center_y += change_y

        # How far are we?
        distance = sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)
        # If we are there, head to the next point.
        if distance <= self.cur_speed:
            
            
            self.cur_position += 1

            # Reached the end of the list, start over.
            if self.cur_position >= len(self.position_list):
                self.cur_position = len(self.position_list) - 1

    def attack(self, target, time_delta):
        if self.current_attack_cooldown > 0:
            self.current_attack_cooldown -= time_delta
        if self.collides_with_sprite(target) and self.current_attack_cooldown <= 0:
            target.update_health(-self.attack_damage)
            self.current_attack_cooldown = self.attack_cooldown
        
