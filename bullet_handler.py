from math import atan2, degrees, cos, sin
from config import SPRITE_SCALING_LASER, BULLET_SPEED, BULLET_DAMAGE, FIELD_BOTTOM_BOUNDARY, FIELD_LEFT_BOUNDARY, FIELD_RIGHT_BOUNDARY, FIELD_TOP_BOUNDARY
from arcade import Sprite, resources, check_for_collision_with_list


class BulletHandler():
    def __init__(self, player, bullet_list, target_list, wall_list):
        self.player = player
        self.bullet_list = bullet_list
        self.target_list = target_list
        self.wall_list = wall_list

    def mouse_press(self, x, y, view_left, view_bottom):
        bullet = Sprite(resources.image_laser_blue01, SPRITE_SCALING_LASER)

        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        dest_x = x + view_left
        dest_y = y + view_bottom

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = atan2(y_diff, x_diff)

        bullet.angle = degrees(angle)

        bullet.change_x = cos(angle) * BULLET_SPEED
        bullet.change_y = sin(angle) * BULLET_SPEED

        self.bullet_list.append(bullet)

    def update(self):
        self.bullet_list.update()
        score_delta = 0
        for bullet in self.bullet_list:

            target_hit_list = check_for_collision_with_list(
                bullet, self.target_list)
            wall_hit_list = check_for_collision_with_list(
                bullet, self.wall_list)

            if len(target_hit_list) > 0 or len(wall_hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for enemy in target_hit_list:
                if not enemy.update_health(-BULLET_DAMAGE):
                    score_delta += 1
                break

            if bullet.bottom > FIELD_TOP_BOUNDARY or bullet.top < FIELD_BOTTOM_BOUNDARY or bullet.right < FIELD_LEFT_BOUNDARY or bullet.left > FIELD_RIGHT_BOUNDARY:
                bullet.remove_from_sprite_lists()

        return score_delta
