import pygame as pg
from ecs import *

FPS = 30


class Engine:

    __world: World
    __system: System

    def __init__(self, world: World, system: System) -> None:
        self.__world = world
        self.__system = system

    def run(self) -> None:
        clock = pg.time.Clock()
        while not self.__system.requests_quit():
            clock.tick(FPS)
            frame_time = Timems(clock.get_time())
            self.__system.run(self.__world, frame_time)
        self.__system.clean()
