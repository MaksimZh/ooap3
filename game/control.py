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


class EmptyTarget(Component):
    pass

empty_target = EmptyTarget()

class ForbiddenTarget(Component):
    pass

forbidden_target = EmptyTarget()

@dataclass
class Target(Component):
    target: Entity


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
                components[EmptyTarget] = empty_target
                return components
            if field.is_cell_obstacle(target_position.x, target_position.y):
                target = field.get_cell_entity(target_position.x, target_position.y)
                components[Target] = Target(target)
                return components
            components[ForbiddenTarget] = forbidden_target
            return components
        
        world.process_entities(
            with_components={Step, FieldPosition},
            no_components={FieldMotion},
            process=process)


class StepSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        def process(components: ComponentDict) -> ComponentDict:
            step: Step = components[Step] #type: ignore
            components[FieldMotion] = FieldMotion(step.direction, 0)
            return components

        world.process_entities(
            with_components={Step, FieldPosition, EmptyTarget},
            no_components={FieldMotion},
            process=process)


class ClearStepSystem(System):

    def run(self, world: World, frame_time: Timems) -> None:
        
        def process(components: ComponentDict) -> ComponentDict:
            del components[Step]
            if Target in components:
                del components[Target]
            if ForbiddenTarget in components:
                del components[ForbiddenTarget]
            if EmptyTarget in components:
                del components[EmptyTarget]
            return components
        
        world.process_entities({Step}, set(), process)
