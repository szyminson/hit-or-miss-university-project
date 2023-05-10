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
    """
    This class represents the Enemy on our screen.
    """
    def __init__(self, resource, bar_list):
        super().__init__(resource, bar_list)
        self.position_list = [[self.center_x, self.center_y]]
        self.cur_position = 0
        self.speed = 3.0
        self.cur_mode = BehaviourMode.REST
        self.guid = uuid4()
        self.player_offset = randint(-12, 12)

    def next_position(self):
        """ Have a sprite follow a path """
        
        # Where are we
        start_x = self.center_x
        start_y = self.center_y
        """ print(self.position_list)
        print(bool(len(self.position_list) <= self.cur_position)) """
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
        speed = min(self.speed, distance)

        # Calculate vector to travel
        change_x = cos(angle) * speed
        change_y = sin(angle) * speed
        #print(change_x, change_y)
        # Update our location
        self.center_x += change_x
        self.center_y += change_y

        # How far are we?
        distance = sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)
        """ print(self.cur_position, len(self.position_list) - 1) """
        # If we are there, head to the next point.
        if distance <= self.speed:
            
            
            self.cur_position += 1

            # Reached the end of the list, start over.
            if self.cur_position >= len(self.position_list):
                self.cur_position = len(self.position_list) - 1
