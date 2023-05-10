from arcade import Sprite
from utilities.indicator_bar import IndicatorBar
from config import SPRITE_SCALING


class KillableSprite(Sprite):
    def __init__(self, resource, bar_list):
        super().__init__(resource, SPRITE_SCALING)
        self.indicator_bar: IndicatorBar = IndicatorBar(
            self, bar_list, (self.center_x, self.center_y)
        )
        self.health: int = 100

    def update_bar_position(self):
        self.indicator_bar.position = (
            self.center_x,
            self.center_y + int(self.height/2) + 1,
        )
