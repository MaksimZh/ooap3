import pygame as pg
from ecs import *

FPS = 30
BACKGROUND_COLOR = (0, 0, 32)


class GraphicsSystem(System):

    __screen: pg.Surface

    def __init__(self) -> None:
        pg.display.init()
        self.__screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    def run(self, world: World, frame_time: Timems) -> None:
        self.__screen.fill(BACKGROUND_COLOR)
        pg.display.update()

    def clean(self) -> None:
        pg.display.quit()

    def requests_quit(self) -> bool:
        return False
    

class InputSystem(System):

    __requests_quit: bool

    def __init__(self) -> None:
        self.__requests_quit = False

    def run(self, world: World, frame_time: Timems) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__requests_quit = True

    def clean(self) -> None:
        pass

    def requests_quit(self) -> bool:
        return self.__requests_quit


class SystemList(System):
    
    __systems: list[System]
    __requests_quit: bool

    def __init__(self) -> None:
        self.__systems = []
        self.__requests_quit = False

    def add(self, system: System) -> None:
        assert system not in self.__systems
        self.__systems.append(system)

    def run(self, world: World, frame_time: Timems) -> None:
        for system in self.__systems:
            system.run(world, frame_time)
            self.__requests_quit = \
                self.__requests_quit or system.requests_quit()

    def clean(self) -> None:
        for system in self.__systems:
            system.clean()
    
    def requests_quit(self) -> bool:
        return self.__requests_quit


class Engine:

    __world: World
    __systems: SystemList

    def __init__(self, world: World, systems: SystemList) -> None:
        self.__world = world
        self.__systems = systems

    def run(self) -> None:
        clock = pg.time.Clock()
        while not self.__systems.requests_quit():
            clock.tick(FPS)
            frame_time = Timems(clock.get_time())
            self.__systems.run(self.__world, frame_time)
        self.__systems.clean()


world = World()
systems = SystemList()
systems.add(InputSystem())
systems.add(GraphicsSystem())
engine = Engine(world, systems)
engine.run()
