from ecs import *
from field import GameField, FieldPosition, FieldMotion, calc_target
from control import Step

class Exit(Component):
    pass

class ExitStepSystem(System):

    __end: bool

    def __init__(self) -> None:
        self.__end = False

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
        if not field.is_cell_obstacle(target_position.x, target_position.y):
            return
        target = field.get_cell_entity(target_position.x, target_position.y)
        if not world.has_component(target, Exit):
            return
        self.__end = True

    def requests_quit(self) -> bool:
        return self.__end
