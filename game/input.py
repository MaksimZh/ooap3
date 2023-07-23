from dataclasses import dataclass
import pygame as pg
from ecs import *
from base import *


class PlayerControl(Component):
    pass

@dataclass
class Command(Component):
    direction: Direction
    single: bool

key_directions = {
    pg.K_UP: Direction.UP,
    pg.K_DOWN: Direction.DOWN,
    pg.K_LEFT: Direction.LEFT,
    pg.K_RIGHT: Direction.RIGHT,
}

class InputSystem(System):

    __requests_quit: bool

    def __init__(self) -> None:
        self.__requests_quit = False

    def run(self, world: World, frame_time: Timems) -> None:
        for event in pg.event.get():
            self.__process_event(world, event)

    def requests_quit(self) -> bool:
        return self.__requests_quit
    
    def __process_event(self, world: World, event: pg.event.Event) -> None:
        match event.type:
            case pg.QUIT:
                self.__requests_quit = True
            case pg.KEYDOWN:
                self.__process_key_down(world, event.key)
            case pg.KEYUP:
                self.__process_key_up(world, event.key)
            case _:
                pass
        
    def __process_key_down(self, world: World, key: int) -> None:
        if not key in key_directions:
            return
        heroes = world.get_entities({PlayerControl}, set())
        if heroes.is_empty():
            return
        hero = heroes.get_entity()
        if not world.has_component(hero, Command):
            world.add_component(hero, Command(Direction.UP, False))
        command: Command = world.get_component(hero, Command) #type: ignore
        command.direction = key_directions[key]
        command.single = False

    def __process_key_up(self, world: World, key: int) -> None:
        if not key in key_directions:
            return
        heroes = world.get_entities({PlayerControl}, set())
        if heroes.is_empty():
            return
        hero = heroes.get_entity()
        if not world.has_component(hero, Command):
            return
        command: Command = world.get_component(hero, Command) #type: ignore
        if command.direction == key_directions[key]:
            command.single = True
