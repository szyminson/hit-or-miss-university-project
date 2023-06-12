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
        # Create a bullet
        bullet = Sprite(resources.image_laser_blue01, SPRITE_SCALING_LASER)

        # Position the bullet at the player's current location
        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x + view_left
        dest_y = y + view_bottom

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        bullet.angle = degrees(angle)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = cos(angle) * BULLET_SPEED
        bullet.change_y = sin(angle) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def update(self):
        # Call update on all sprites
        self.bullet_list.update()
        score_delta = 0
        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            target_hit_list = check_for_collision_with_list(
                bullet, self.target_list)
            wall_hit_list = check_for_collision_with_list(
                bullet, self.wall_list)

            # If it did, get rid of the bullet
            if len(target_hit_list) > 0 or len(wall_hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for enemy in target_hit_list:
                if not enemy.update_health(-BULLET_DAMAGE):
                    score_delta += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > FIELD_TOP_BOUNDARY or bullet.top < FIELD_BOTTOM_BOUNDARY or bullet.right < FIELD_LEFT_BOUNDARY or bullet.left > FIELD_RIGHT_BOUNDARY:
                bullet.remove_from_sprite_lists()

        return score_delta
