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
        screen_set = world.get_entities({ScreenSize}, set())
        if screen_set.is_empty():
            self.__add_screen_size(world)
        self.__screen.fill(BACKGROUND_COLOR)
        entities = world.get_entities({Sprite, ScreenPosition}, set())
        while not entities.is_empty():
            e = entities.get_entity()
            sprite: Sprite = world.get_component(e, Sprite) #type: ignore
            pos: ScreenPosition = world.get_component(e, ScreenPosition) #type: ignore
            self.__screen.blit(sprite.source, (pos.x, pos.y), sprite.rect)
            entities.remove_entity(e)
        pg.display.update()

    def clean(self) -> None:
        if not pg.display.get_init():
            return
        pg.display.quit()

    def requests_quit(self) -> bool:
        return False
    
    def __add_screen_size(self, world: World) -> None:
        screen = world.new_entity()
        world.add_entity(screen)
        width, height = self.__screen.get_size()
        world.add_component(screen, ScreenSize(width, height))
