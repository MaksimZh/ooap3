from dataclasses import dataclass
from ecs import *
from base import *
from input import Command
from field import GameField, FieldPosition, FieldMotion, calc_target

@dataclass
class Step(Component):
    direction: Direction

class ControlSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        heroes = world.get_entities({Command, FieldPosition}, set())
        if heroes.is_empty():
            return
        hero = heroes.get_entity()
        command: Command = world.get_component(hero, Command) #type: ignore
        if command.single:
            world.remove_component(hero, Command)
        if world.has_component(hero, FieldMotion):
            return
        if world.has_component(hero, Step):
            return
        world.add_component(hero, Step(command.direction))


class StepSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        field: GameField = world.get_component(world.get_global_entity(), GameField) #type: ignore
        if world.is_status("get_component", "NO_COMPONENT"):
            return
        heroes = world.get_entities({Step, FieldPosition}, set())
        if heroes.is_empty():
            return
        hero = heroes.get_entity()
        if world.has_component(hero, FieldMotion):
            return
        position: FieldPosition = world.get_component(hero, FieldPosition) #type: ignore
        step: Step = world.get_component(hero, Step) #type: ignore
        target_position = calc_target(position, step.direction)
        if field.is_cell_empty(target_position.x, target_position.y):
            world.add_component(hero, FieldMotion(step.direction, 0))
            return

class ClearStepSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        heroes = world.get_entities({Step, FieldPosition}, set())
        if heroes.is_empty():
            return
        hero = heroes.get_entity()
        world.remove_component(hero, Step)
