from dataclasses import dataclass
from ecs import *
from base import *
from input import Command
from field import FieldPosition, FieldMotion

@dataclass
class Step:
    direction: Direction

class ControlSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        hero = world.get_single_entity({Command, FieldPosition})
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return
        if not world.has_component(hero, Command):
            return
        command: Command = world.get_component(hero, Command) #type: ignore
        if command.single:
            world.remove_component(hero, Command)
        if world.has_component(hero, FieldMotion):
            return
        world.add_component(hero, FieldMotion(command.direction, 0))
