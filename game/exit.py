from ecs import *
from field import FieldPosition, FieldMotion
from control import Step, Target

class Exit(Component):
    pass

class ExitStepSystem(System):

    __end: bool

    def __init__(self) -> None:
        self.__end = False

    def run(self, world: World, frame_time: Timems) -> None:
        
        def process(components: ComponentDict) -> ComponentDict:
            target_component: Target = components[Target] #type: ignore
            target = target_component.target
            if world.has_component(target, Exit):
                self.__end = True
            return components

        world.process_entities(
            with_components={Step, FieldPosition, Target},
            no_components={FieldMotion},
            process=process)

    def requests_quit(self) -> bool:
        return self.__end
