from random import randint
from arcade import Sprite, has_line_of_sight, astar_calculate_path, AStarBarrierList, PhysicsEngineSimple
from sprites.enemy import BehaviourMode, Enemy
import config
from pickle import load
import os


class EnemyMovementController():
    def __init__(self, enemy_list, player, wall_list):
        self.enemy_list = enemy_list
        self.player = player
        self.wall_list = wall_list
        self.barrier_list_per_size = {}
        self.physics_engines = {}
        with open(os.path.join(os.path.dirname(__file__), 'model.pkl'), 'rb') as f:
            self.clf = load(f)

    def update(self, time_delta):
        self.update_modes()
        self.handle_modes(time_delta)
        self.update_positions()

    def handle_modes(self, time_delta):
        for enemy in self.enemy_list:
            if enemy.cur_mode == BehaviourMode.ATTACK:
                self.handle_attack(enemy, time_delta)
            elif enemy.cur_mode == BehaviourMode.REST:
                self.handle_rest(enemy, time_delta)
            elif enemy.cur_mode == BehaviourMode.PANIC:
                self.handle_panic(enemy, time_delta)

    def handle_rest(self, enemy: Enemy, time_delta):
        return
    
    def handle_panic(self, enemy: Enemy, time_delta):
        if not len(enemy.position_list):
            x = randint(config.FIELD_LEFT_BOUNDARY, config.FIELD_RIGHT_BOUNDARY)
            y = randint(config.FIELD_BOTTOM_BOUNDARY, config.FIELD_TOP_BOUNDARY)
            self.set_path_to_point(enemy, (x, y))
        enemy.cur_speed = enemy.panic_speed
    
    def is_in_player_view(self, enemy: Sprite) -> bool:
        in_view = False
        try:
            in_view = has_line_of_sight(self.player.position,
                                enemy.position,
                                self.wall_list)
        except ZeroDivisionError:
            in_view = True
        return in_view
    
    def handle_attack(self, enemy: Enemy, time_delta):
        enemy.attack(self.player, time_delta)
        
        if self.is_in_player_view(enemy):
            enemy.cur_speed = enemy.charge_speed
        else:
            enemy.cur_speed = enemy.cur_speed
        self.set_path_to_point(enemy, self.player.position)
    
    def set_path_to_point(self, enemy, point):
        barrier_list = self.get_barrier_list(enemy)
        enemy.position_list = astar_calculate_path(enemy.position,
                                                    point,
                                                    barrier_list,
                                                    diagonal_movement=False)
        final_position = tuple(x + enemy.player_offset for x in point)
        if enemy.position_list:
            enemy.position_list.append(final_position)
        else:
            enemy.position_list = [final_position]
        if len(enemy.position_list) <= enemy.cur_position:
            enemy.cur_position = 0

    def update_modes(self):
        player_heath = self.player.health / self.player.max_health
        for enemy in self.enemy_list:
            health = enemy.health / enemy.max_health
            in_sight = int(self.is_in_player_view(enemy))
            friends = len(self.enemy_list) - 1
            mode_number = self.clf.predict([[health, friends, in_sight, player_heath]])[0]
            previous_mode = enemy.cur_mode
            enemy.cur_mode = BehaviourMode(mode_number)
            if previous_mode != enemy.cur_mode:
                print([health, friends, in_sight, player_heath])
                print(enemy.cur_mode)
                enemy.position_list = []

    def update_positions(self):
        self.ensure_physics_engines()
        for engine in self.physics_engines.values():
            engine.player_sprite.next_position()
            engine.player_sprite.update_bar_position()
            engine.update()

    def ensure_physics_engines(self):
        for enemy in self.enemy_list:
            if not enemy.guid in self.physics_engines.keys():
                self.physics_engines[enemy.guid] = PhysicsEngineSimple(enemy, self.wall_list)

    def get_barrier_list(self, enemy):
        key = str(enemy.width) + 'x' + str(enemy.height)
        if key not in self.barrier_list_per_size.keys():
            self.barrier_list_per_size[key] = AStarBarrierList(enemy,
                                                               self.wall_list,
                                                               config.SPRITE_SIZE,
                                                               config.FIELD_LEFT_BOUNDARY,
                                                               config.FIELD_RIGHT_BOUNDARY,
                                                               config.FIELD_BOTTOM_BOUNDARY,
                                                               config.FIELD_TOP_BOUNDARY)
        return self.barrier_list_per_size[key]
