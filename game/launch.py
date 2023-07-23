import sys
import pygame as pg

import ecs
import engine as eg
from input import InputSystem, PlayerControl
from graphics import Sprite, GraphicsSystem
from field import GameField, FieldPosition, CameraFollow, CameraSystem, MotionSystem
from control import ControlSystem, StepSystem, ClearStepSystem
from consume import Consumable, ConsumeStepSystem, ConsumeSystem
from exit import Exit, ExitStepSystem

game_path = sys.path[0]
sprites = pg.image.load(game_path + "/sprites.png")


components = {
    "@": [
        Sprite(sprites, pg.Rect(0, 0, 48, 48)),
        PlayerControl(),
        CameraFollow(),
    ],
    "W": [
        Sprite(sprites, pg.Rect(0, 48, 48, 48)),
    ],
    "+": [
        Sprite(sprites, pg.Rect(0, 48 * 2, 48, 48)),
        Consumable(),
    ],
    "E": [
        Sprite(sprites, pg.Rect(48, 0, 48, 48)),
        Exit(),
    ],
}

level = [
    "+++++++++E",
    "++++++++++",
    "++++++++++",
    "...WWW+.+.",
    "...+@...+.",
    "...WWW+.+.",
    "++++++++++",
    "++++++++++",
    "++++++++++",
    "++++++++++",
]


world = ecs.World()
field = GameField(len(level[0]), len(level))
world.add_component(world.get_global_entity(), field)

for y in range(len(level)):
    for x in range(len(level[0])):
        cell = level[y][x]
        if cell not in components:
            continue
        e = world.new_entity()
        world.add_component(e, FieldPosition(x, y))
        field.set_cell(x, y, e)
        for c in components[cell]:
            world.add_component(e, c)

systems = ecs.SystemList()
systems.add(MotionSystem())
systems.add(InputSystem())
systems.add(ControlSystem())
systems.add(StepSystem())
systems.add(ConsumeStepSystem())
systems.add(ExitStepSystem())
systems.add(ClearStepSystem())
systems.add(ConsumeSystem())
systems.add(CameraSystem())
systems.add(GraphicsSystem())
engine = eg.Engine(world, systems)
engine.run()
