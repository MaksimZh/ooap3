from dataclasses import dataclass
import pygame as pg
from ecs import *

BACKGROUND_COLOR = (0, 0, 32)

@dataclass
class ScreenSize(Component):
    width: int
    height: int

@dataclass
class ScreenPosition(Component):
    x: int
    y: int

@dataclass
class Sprite(Component):
    source: pg.Surface
    rect: pg.Rect


class GraphicsSystem(System):

    __screen: pg.Surface

    def __init__(self) -> None:
        pg.display.init()
        self.__screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    def run(self, world: World, frame_time: Timems) -> None:
        if not world.has_component(world.get_global_entity(), ScreenSize):
            self.__add_screen_size(world)
        self.__screen.fill(BACKGROUND_COLOR)
        world.process_entities({Sprite, ScreenPosition}, set(), self.__draw)
        pg.display.update()

    def clean(self) -> None:
        if not pg.display.get_init():
            return
        pg.display.quit()

    def __draw(self, components: ComponentDict) -> ComponentDict:
        sprite: Sprite = components[Sprite] #type: ignore
        pos: ScreenPosition = components[ScreenPosition] #type: ignore
        self.__screen.blit(sprite.source, (pos.x, pos.y), sprite.rect)
        return components

    def __add_screen_size(self, world: World) -> None:
        width, height = self.__screen.get_size()
        world.add_component(world.get_global_entity(), ScreenSize(width, height))
