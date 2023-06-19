"""
A-Star Path-finding

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.astar_pathfinding
"""

import arcade
import random
from bullet_handler import BulletHandler

import config
from enemy_movement import EnemyMovementController
from enemy_spawner import EnemySpawner
from sprites.robot import Robot
from sprites.zombie import Zombie
from sprites.player import Player

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        super().__init__(width, height, title)

        self.player_list = None
        self.wall_list = None
        self.enemy_list = None
        self.bar_list = None
        self.bullet_list = None

        self.player = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.physics_engine = None
        self.enemy_movement_controller = None
        self.bullet_handler = None
        self.enemy_spawner = None

        self.path = None
        self.barrier_list = None

        self.view_bottom = 0
        self.view_left = 0

        self.background_color = arcade.color.AMAZON

        self.score = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True,
                                           spatial_hash_cell_size=128)
        self.enemy_list = arcade.SpriteList()
        self.bar_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = Player(self.bar_list)
        self.player_list.append(self.player)


        spacing = config.SPRITE_SIZE * 3
        for column in range(10):
            for row in range(15):
                sprite = arcade.Sprite(arcade.resources.image_box_crate_single,
                                       config.SPRITE_SCALING)

                x = (column + 1) * spacing
                y = (row + 1) * sprite.height

                sprite.center_x = x
                sprite.center_y = y
                if random.randrange(100) > 70:
                    self.wall_list.append(sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.wall_list)

        self.path = None

        self.enemy_movement_controller = EnemyMovementController(
            self.enemy_list, self.player, self.wall_list)
        self.bullet_handler = BulletHandler(self.player, self.bullet_list, self.enemy_list, self.wall_list)
        self.enemy_spawner = EnemySpawner(self.enemy_list, self.wall_list, self.bar_list)

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()

        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.bar_list.draw()
        self.bullet_list.draw()

        output = f"Score: {self.score} Enemies left: {len(self.enemy_list)}"
        if self.player.health <= 0:
            output = f"GAME OVER! Score: {self.score}"
        arcade.draw_text(output, 10 + self.view_left, 20 + self.view_bottom, arcade.color.WHITE, 16)
            
        """ if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2) """

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.player.change_x = 0
        self.player.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player.change_y = config.MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -config.MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -config.MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = config.MOVEMENT_SPEED

        self.physics_engine.player_sprite.update_bar_position()
        self.physics_engine.update()
        self.enemy_movement_controller.update(delta_time)
        self.score += self.bullet_handler.update()

        changed = False

        left_boundary = self.view_left + config.VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        right_boundary = self.view_left + config.SCREEN_WIDTH - config.VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + config.SCREEN_HEIGHT - config.VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + config.VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        if changed:
            arcade.set_viewport(self.view_left,
                                config.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                config.SCREEN_HEIGHT + self.view_bottom)
        self.enemy_spawner.update(delta_time)
            
    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """
        if self.player.health <= 0:
            return
        self.bullet_handler.mouse_press(x,y, self.view_left, self.view_bottom)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if self.player.health <= 0:
            return
        if key in [arcade.key.UP, arcade.key.W]:
            self.up_pressed = True
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.down_pressed = True
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = True
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if self.player.health <= 0:
            return
        if key in [arcade.key.UP, arcade.key.W]:
            self.up_pressed = False
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.down_pressed = False
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = False
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = False


def main():
    """ Main function """
    window = MyGame(config.SCREEN_WIDTH,
                    config.SCREEN_HEIGHT, config.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
