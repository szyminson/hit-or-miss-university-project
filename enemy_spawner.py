
from sprites.robot import Robot
from sprites.zombie import Zombie
import config
from random import randint, randrange
from arcade import check_for_collision_with_list


class EnemySpawner():
    enemy_types = [Zombie, Robot]
    def __init__(self, enemy_list, wall_list, bar_list):
        self.enemy_list = enemy_list
        self.wall_list = wall_list
        self.bar_list = bar_list
        self.next_spawn_in = 2
    
    def update(self, time_delta):
        self.next_spawn_in -= time_delta
        if self.next_spawn_in <= 0:
            enemy_count = len(self.enemy_list)
            if enemy_count < config.ENEMY_LIMIT:
                for _ in range(randint(1, config.ENEMY_LIMIT-enemy_count)):
                    enemy_type = randint(0,1)
                    self.spawn_enemy(enemy_type)
            self.next_spawn_in = randint(15, 30)
                
    def spawn_enemy(self, type):
        enemy = self.enemy_types[type](self.bar_list)
        while True:
            initial_x = randrange(config.SCREEN_WIDTH)
            initial_y = randrange(config.SCREEN_HEIGHT)
            enemy.center_x = initial_x
            enemy.center_y = initial_y
            if not check_for_collision_with_list(enemy, self.wall_list):
                break
        self.enemy_list.append(enemy)

