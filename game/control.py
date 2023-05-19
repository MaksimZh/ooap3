from dataclasses import dataclass
from ecs import *
from base import *
from input import Command
from field import GameField, FieldPosition, FieldMotion, calc_target

@dataclass
class Step:
    direction: Direction

class ControlSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        hero = world.get_single_entity({Command, FieldPosition})
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return
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
        field_entity = world.get_single_entity({GameField})
        field: GameField = world.get_component(field_entity, GameField) #type: ignore
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return
        hero = world.get_single_entity({Step, FieldPosition})
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return
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
        hero = world.get_single_entity({Step, FieldPosition})
        if world.is_status("get_single_entity", "NOT_FOUND"):
            return
        world.remove_component(hero, Step)
