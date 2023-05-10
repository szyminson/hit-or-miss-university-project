"""
A-Star Path-finding

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.astar_pathfinding
"""

import arcade
import random

import config
from enemy_movement import EnemyMovementController
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

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None
        self.wall_list = None
        self.enemy_list = None
        self.bar_list = None

        # Set up the player info
        self.player = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.physics_engine = None
        self.enemy_movement_controller = None

        # --- Related to paths
        # List of points that makes up a path between two points
        self.path = None
        # List of points we checked to see if there is a barrier there
        self.barrier_list = None

        # Used in scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Set the window background color
        self.background_color = arcade.color.AMAZON

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True,
                                           spatial_hash_cell_size=128)
        self.enemy_list = arcade.SpriteList()
        self.bar_list = arcade.SpriteList()

        # Set up the player

        self.player = Player(self.bar_list)
        self.player_list.append(self.player)

        # Set enemies
        for i in range(4):
            while True:
                initial_x = random.randrange(config.SCREEN_WIDTH)
                initial_y = random.randrange(config.SCREEN_HEIGHT)
                enemy = Zombie(self.bar_list)
                enemy.center_x = initial_x
                enemy.center_y = initial_y
                if not arcade.check_for_collision_with_list(enemy, self.wall_list):
                    self.enemy_list.append(enemy)
                    break
            print(i)

        spacing = config.SPRITE_SIZE * 3
        for column in range(10):
            for row in range(15):
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_single.png",
                                       config.SPRITE_SCALING)

                x = (column + 1) * spacing
                y = (row + 1) * sprite.height

                sprite.center_x = x
                sprite.center_y = y
                if random.randrange(100) > 70:
                    self.wall_list.append(sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.wall_list)

        # --- Path related
        # This variable holds the travel-path. We keep it as an attribute so
        # we can calculate it in on_update, and draw it in on_draw.
        self.path = None

        self.enemy_movement_controller = EnemyMovementController(
            self.enemy_list, self.player, self.wall_list)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.bar_list.draw()

        for enemy in self.enemy_list:
            """ print("draw") """
            #print(enemy.position, enemy.position_list[-1], self.player.position)
            if self.player.position != enemy.position and arcade.has_line_of_sight(self.player.position,
                                                                                   enemy.position,
                                                                                   self.wall_list):
                color = arcade.color.RED
            else:
                color = arcade.color.WHITE
            arcade.draw_line(self.player.center_x,
                             self.player.center_y,
                             enemy.center_x,
                             enemy.center_y,
                             color,
                             2)
        """ if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2) """

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player.change_x = 0
        self.player.change_y = 0
        """ print("on update") """
        #print(delta_time)

        if self.up_pressed and not self.down_pressed:
            self.player.change_y = config.MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -config.MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -config.MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = config.MOVEMENT_SPEED

        # Update the character
        self.physics_engine.player_sprite.update_bar_position()
        self.physics_engine.update()
        self.enemy_movement_controller.update()
        # print(self.path,"->", self.player.position)

        # --- Manage Scrolling ---

        # Keep track of if we changed the boundary. We don't want to call the
        # set_viewport command if we didn't change the view port.
        changed = False

        # Scroll left
        left_boundary = self.view_left + config.VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + config.SCREEN_WIDTH - config.VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + config.SCREEN_HEIGHT - config.VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + config.VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                config.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                config.SCREEN_HEIGHT + self.view_bottom)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """ Main function """
    window = MyGame(config.SCREEN_WIDTH,
                    config.SCREEN_HEIGHT, config.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
