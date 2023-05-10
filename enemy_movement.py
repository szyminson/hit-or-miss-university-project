from random import randint
from arcade import has_line_of_sight, astar_calculate_path, AStarBarrierList, PhysicsEngineSimple
from sprites.enemy import BehaviourMode
from config import SPRITE_SIZE, FIELD_LEFT_BOUNDARY, FIELD_RIGHT_BOUNDARY, FIELD_TOP_BOUNDARY, FIELD_BOTTOM_BOUNDARY


class EnemyMovementController():
    def __init__(self, enemy_list, player, wall_list):
        self.enemy_list = enemy_list
        self.player = player
        self.wall_list = wall_list
        self.barrier_list_per_size = {}
        self.physics_engines = {}

    def update(self):
        self.update_modes()
        self.update_positions()

    def update_modes(self):
        for enemy in self.enemy_list:
            in_view = False
            try:
                in_view = has_line_of_sight(self.player.position,
                                 enemy.position,
                                 self.wall_list)
            except ZeroDivisionError:
                in_view = True
            if in_view:
                enemy.cur_mode = BehaviourMode.ATTACK
                barrier_list = self.get_barrier_list(enemy)
                enemy.position_list = astar_calculate_path(enemy.position,
                                                           self.player.position,
                                                           barrier_list,
                                                           diagonal_movement=False)
                final_position = tuple(x + enemy.player_offset for x in self.player.position)
                if enemy.position_list:
                    enemy.position_list.append(final_position)
                else:
                    enemy.position_list = [final_position]
                if len(enemy.position_list) <= enemy.cur_position:
                    enemy.cur_position = 0
            else:
                enemy.cur_mode = BehaviourMode.REST

    def update_positions(self):
        self.ensure_physics_engines()
        for engine in self.physics_engines.values():
            engine.player_sprite.next_position()
            engine.player_sprite.update_bar_position()
            engine.update()

    def ensure_physics_engines(self):
        for enemy in self.enemy_list:
            #print(enemy.guid)
            if not enemy.guid in self.physics_engines.keys():
                self.physics_engines[enemy.guid] = PhysicsEngineSimple(enemy, self.wall_list)

    def get_barrier_list(self, enemy):
        key = str(enemy.width) + 'x' + str(enemy.height)
        if key not in self.barrier_list_per_size.keys():
            #print('calcing for '+ key)
            self.barrier_list_per_size[key] = AStarBarrierList(enemy,
                                                               self.wall_list,
                                                               SPRITE_SIZE,
                                                               FIELD_LEFT_BOUNDARY,
                                                               FIELD_RIGHT_BOUNDARY,
                                                               FIELD_BOTTOM_BOUNDARY,
                                                               FIELD_TOP_BOUNDARY)
        return self.barrier_list_per_size[key]
