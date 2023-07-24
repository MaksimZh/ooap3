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
        world.process_entities({Command, FieldPosition}, set(), self.__process)

    def __process(self, components: ComponentDict) -> ComponentDict:
        command: Command = components[Command] #type: ignore
        if command.single:
            del components[Command]
        if FieldMotion in components or Step in components:
            return components
        components[Step] = Step(command.direction)
        return components


class ForbiddenTarget:
    pass

forbidden_target = ForbiddenTarget()

@dataclass
class Target(Component):
    target: None | Entity | ForbiddenTarget

class TargetSystem(System):
    
    def run(self, world: World, frame_time: Timems) -> None:
        field: GameField = world.get_component(world.get_global_entity(), GameField) #type: ignore
        if world.is_status("get_component", "NO_COMPONENT"):
            return
        
        def process(components: ComponentDict) -> ComponentDict:
            position: FieldPosition = components[FieldPosition] #type: ignore
            step: Step = components[Step] #type: ignore
            target_position = calc_target(position, step.direction)
            if field.is_cell_empty(target_position.x, target_position.y):
                components[Target] = Target(None)
                return components
            if not field.is_cell_obstacle(target_position.x, target_position.y):
                components[Target] = Target(forbidden_target)
                return components
            target = field.get_cell_entity(target_position.x, target_position.y)
            components[Target] = Target(target)
            return components
        
        world.process_entities(
            with_components={Step, FieldPosition},
            no_components={FieldMotion},
            process=process)


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
        
        def process(components: ComponentDict) -> ComponentDict:
            del components[Step]
            del components[Target]
            return components
        
        world.process_entities({Step, Target}, set(), process)
