from arcade import Sprite
from utilities.indicator_bar import IndicatorBar
from config import SPRITE_SCALING


class KillableSprite(Sprite):
    max_health: int = 100
    
    def __init__(self, resource, bar_list):
        super().__init__(resource, SPRITE_SCALING)
        self.indicator_bar: IndicatorBar = IndicatorBar(
            self, bar_list, (self.center_x, self.center_y)
        )
        self.health: int = self.max_health

    def update_bar_position(self):
        self.indicator_bar.position = (
            self.center_x,
            self.center_y + int(self.height/2) + 1,
        )
    
    def update_health(self, delta: int, remove: bool = True) -> bool:
        self.health += delta
        fullness = self.health / self.max_health
        fullness = 0 if fullness < 0 else fullness
        self.indicator_bar.fullness = fullness
        alive = True
        if self.health <= 0:
            if remove:
                self.remove_from_sprite_lists()
                self.indicator_bar.delete()
            alive = False
        return alive
