import pygame as pg
from ecs import *

FPS = 30
BACKGROUND_COLOR = (0, 0, 32)


class InputEngine:
    ...


class Engine:

    __screen: pg.Surface

    def __init__(self) -> None:
        pg.init()
        self.__screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    def run(self) -> None:
        running = True
        clock = pg.time.Clock()
        while running:
            clock.tick(FPS)
            frame_time = Timems(clock.get_time())
            self.frame(frame_time)
            self.__screen.fill(BACKGROUND_COLOR)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
        pg.quit()

    def frame(self, time_ms: int) -> None:
        print(time_ms)

Engine().run()
