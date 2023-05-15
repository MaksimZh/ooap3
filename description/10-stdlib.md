# Стандартная библиотека

## Ядро ECS
В отдельную библиотеку можно выделить классы, которые обеспечивают базовую
работу ECS:
- `World` - игровой мир, содержащий все сущности, компоненты и их связи;
- `EntitySet` - подмножество сущностей игрового мира, получаемое при фильтрации.

Туда же стоит добавить классы, являющиеся базовыми для льготного наследования:
- `Component` - базовый класс для всех компонентов;
- `System` - базовый класс для всех систем.

Движку игры тоже сюда дорога.
Подсчёт времени и запуск систем тесно связаны.


## Графика
Класс `Renderer` реализует набор методов, которые будут нужны любой двумерной игре:
- очистка экрана;
- отображение спрайтов;
- отображение текста;
- переключение буфера (flip).


## Игровое поле
Пока не ясно будут ли это классы `GameField` и `GameWorld`,
или я всё же сделаю выбор в пользу набора компонентов, которые связываются в граф
(более сложная в реализации, но более гибкая и устойчивая архитектура).
В любом случае эти наработки можно будет использовать во всех играх,
где есть прямоугольное поле.
Если использовать граф, то не только прямоугольное, но и гексагональное или
вообще поле-граф как в некоторых играх про войны муравейников
или космических систем.