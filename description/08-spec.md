# Классы поведения


## `World`


### CONSTRUCTOR()
Создаёт пустой игровой мир


### Команды

#### `add_entity()`
добавить новую сущность
- POST: добавлена новая сущность без компонентов;

#### `remove_entity(entity: Entity)`
удалить сущность
- PRE: сущность `entity` присутствует в мире;
- POST: сущность `entity` и связанные с ней компоненты удалены из мира;

#### `add_component(entity: Entity, component: Component)`
добавить компонент к сущности
- PRE: сущность `entity` присутствует в мире;
- PRE: у сущности `entity` нет компонента того же типа что и `component`;
- POST: к сущности `entity` добавлен компонент `component`;

#### `remove_component(entity: Entity, component_type: Type[Component])`
удалить компонент у сущности
- PRE: сущность `entity` присутствует в мире;
- PRE: у сущности `entity` есть компонент типа `component_type`;
- POST: к сущности `entity` добавлен компонент `component`;


### Запросы

#### `is_empty() -> bool`
проверить пуст ли мир

#### `has_entity(entity: Entity) -> bool`
проверить присутствует ли сущность в мире

#### `get_last_entity() -> Entity`
получить последнюю созданную сущность
- PRE: последней командой была `add_entity`;

#### `has_component(entity: Entity, component_type: Type[Component]) -> bool`
проверить есть ли у сущности компонент заданного типа
- PRE: сущность `entity` присутствует в мире;

#### `get_component(entity: Entity, component_type: Type[Component]) -> component`
получить компонент заданного типа у сущности
- PRE: сущность `entity` присутствует в мире;
- PRE: у сущности `entity` есть компонент типа `component_type`;

#### `get_entities(with_components: set[Component], no_components: set[Component]) -> EntitySet`
получить подмножество сущностей со всеми компонентами из `with_components`
и без единого компонента из `no_components`


## `EntitySet`
Абстрактный класс. Конструктор не нужен.


### Команды

#### `remove_entity(entity: Entity)`
удалить сущность
- PRE: сущность `entity` присутствует во множестве;
- POST: сущность `entity` удалена из множества;


### Запросы

#### `is_empty() -> bool`
проверить пусто ли множество

#### `has_entity(entity: Entity) -> bool`
проверить присутствует ли сущность во множестве

#### `get_entity() -> Entity`
получить произвольную сущность из множества
- PRE: множество не пусто;


## `ExtendableEntitySet(EntitySet)`

### CONSTRUCTOR()
Создаёт пустое множество


### Команды

#### `add_entity(entity: Entity)`
добавить сущность
- PRE: сущность `entity` отсутствует во множестве;
- POST: сущность `entity` добавлена во множество;


## GameField

### CONSTRUCTOR(width: int, height: int)
создаёт пустое поле заданного размера


### Команды

#### set(x: int, y: int, entity: Entity)

#### set_coming(x: int, y: int, entity: Entity)


### Запросы

#### get(x: int, y: int) -> Entity

#### get_coming(x: int, y: int) -> Entity

