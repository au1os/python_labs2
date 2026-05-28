# Лабораторная работа №4 - Интерфейсы и абстрактные классы (ABC)
## Вариант 9 (продолжение)

### 1. Цель работы
Познакомиться с абстрактными базовыми классами (ABC), освоить понятие интерфейса (контракта поведения), научиться задавать обязательные методы для классов, закрепить полиморфизм через единый интерфейс, научиться проектировать архитектуру, а не просто классы.

### 2. Описание интерфейсов

#### Интерфейс `IPrintable`
**Назначение:** Определяет контракт для объектов, которые могут быть представлены в виде строки.

**Абстрактные методы:**
- `to_string() -> str` - возвращает строковое представление объекта

**Дополнительные методы:**
- `print_info()` - выводит информацию об объекте в консоль

#### Интерфейс `IComparable`
**Назначение:** Определяет контракт for объектов, которые можно сравнивать между собой.

**Абстрактные методы:**
- `compare_to(other) -> int` - сравнивает текущий объект с другим
  - возвращает отрицательное число, если текущий объект "меньше"
  - возвращает 0, если объекты "равны"
  - возвращает положительное число, если текущий объект "больше"

**Дополнительные методы:**
- `__lt__`, `__le__`, `__gt__`, `__ge__`, `__eq__` - операторы сравнения на основе `compare_to()`

#### Интерфейс `IRentable`
**Назначение:** Определяет контракт для объектов, которые можно сдавать в аренду.

**Абстрактные методы:**
- `get_rental_price() -> float` - возвращает цену аренды
- `is_available() -> bool` - проверяет доступность объекта
- `rent()` - сдаёт объект в аренду
- `vacate()` - освобождает объект

#### Интерфейс `IFilterable`
**Назначение:** Определяет контракт для коллекций, которые поддерживают фильтрацию.

**Абстрактные методы:**
- `filter_by(predicate) -> IFilterable` - фильтрует элементы по предикату
- `get_all() -> List` - возвращает список всех элементов

### 3. Реализация в классах

#### Класс `ApartmentBase`
Базовый класс квартиры, реализующий все интерфейсы:
- `IPrintable.to_string()` - возвращает строковое представление через `__str__()`
- `IComparable.compare_to()` - сравнивает по цене
- `IRentable.get_rental_price()` - возвращает ежемесячный платёж
- `IRentable.is_available()` - проверяет флаг `_is_rented`
- `IRentable.rent()` / `vacate()` - использует методы базового класса

#### Класс `StudioApartment`
Квартира-студия, наследуется от `ApartmentBase`:
- `IPrintable.to_string()` - переопределён с добавлением информации о студии
- `IComparable.compare_to()` - переопределён, сравнивает по площади
- `IRentable.get_rental_price()` - переопределён с учётом типа студии

#### Класс `LuxuryApartment`
Элитная квартира, наследуется от `ApartmentBase`:
- `IPrintable.to_string()` - переопределён с добавлением информации об элитности
- `IComparable.compare_to()` - переопределён, сравнивает по количеству особенностей
- `IRentable.get_rental_price()` - переопределён с учётом элитности

#### Класс `ApartmentCollection`
Коллекция, реализующая интерфейс `IFilterable`:
- `IFilterable.filter_by()` - фильтрует элементы по предикату
- `IFilterable.get_all()` - возвращает копию списка элементов

**Дополнительные методы для работы с интерфейсами:**
- `get_printable()` - возвращает список объектов, реализующих `IPrintable`
- `get_comparable()` - возвращает список объектов, реализующих `IComparable`
- `get_rentable()` - возвращает список объектов, реализующих `IRentable`
- `print_all_items()` - выводит информацию обо всех объектах (через `IPrintable`)
- `sort_by_comparison()` - сортирует через `IComparable`
- `get_available_rentals()` - возвращает доступные для аренды (через `IRentable`)
- `calculate_total_rental_income()` - расчёт общего дохода (через `IRentable`)

### 4. Демонстрация работы

#### Сценарий 1: Работа с интерфейсами IPrintable, IComparable, IRentable
- Создание объектов разных типов
- Проверка реализации интерфейсов через `isinstance()`
- Вызов методов `to_string()`, `compare_to()`, `get_rental_price()`, `is_available()`, `rent()`, `vacate()`

#### Сценарий 2: Универсальные функции через интерфейсы
- Универсальная функция печати `print_all_items()` (через `IPrintable`)
- Универсальная функция сортировки `sort_by_comparison()` (через `IComparable`)
- Универсальная функция расчёта дохода `calculate_total_rental_income()` (через `IRentable`)
- Получение доступных для аренды `get_available_rentals()` (через `IRentable`)

#### Сценарий 3: Фильтрация коллекции через интерфейсы
- Фильтрация по интерфейсу `IPrintable`
- Фильтрация по интерфейсу `IComparable`
- Фильтрация по интерфейсу `IRentable`
- Комбинированная фильтрация через `IFilterable.filter_by()`

#### Сценарий 4: Полиморфизм без условий через интерфейсы
- Единый список объектов разных типов
- Вызов одинаковых методов через интерфейсы
- Разное поведение у разных классов
- Демонстрация правильного паттерна (без `if type == ...`)

### 5. Вывод

В ходе лабораторной работы были изучены:
- **Абстрактные базовые классы (ABC)** - создание интерфейсов через `abc.ABC` и `@abstractmethod`
- **Интерфейсы** - определение контрактов поведения через `IPrintable`, `IComparable`, `IRentable`, `IFilterable`
- **Полиморфизм** - работа с разными типами через единый интерфейс
- **Множественная реализация интерфейсов** - классы реализуют несколько интерфейсов одновременно
- **Архитектурное проектирование** - проектирование системы через интерфейсы, а не через конкретные классы

### 6. Запуск демонстрации

```bash
cd src/lab04
python demo.py
```

### 7. Структура проекта

```
python_labs2/
├── src/
│   ├── lab01/          # Базовый класс Apartment
│   ├── lab02/          # Коллекция ApartmentCollection
│   ├── lab03/          # Наследование и иерархия
│   └── lab04/          # Интерфейсы и абстрактные классы
│       ├── __init__.py
│       ├── interfaces.py # Абстрактные базовые классы (IPrintable, IComparable, IRentable, IFilterable)
│       ├── models.py     # Классы, реализующие интерфейсы
│       ├── collection.py # Коллекция с поддержкой интерфейсов
│       ├── demo.py       # Демонстрация работы
│       └── README.md     # Документация
└── images/
    └── lab04/          # Скриншоты работы программы
```

### 8. Примеры использования

```python
from collection import ApartmentCollection
from interfaces import IPrintable, IComparable, IRentable
from models import ApartmentBase, StudioApartment, LuxuryApartment

# Создание объектов
basic = ApartmentBase(50.0, 100000, "ул. Примерная, 1", 12)
studio = StudioApartment(35.0, 70000, "ул. Студенческая, 5", 6, True, "комфорт")
luxury = LuxuryApartment(120.0, 300000, "пр. Элитный, 1", 12, True, "пентхаус", ["вид на город"])

# Проверка реализации интерфейсов
print(isinstance(basic, IPrintable))    # True
print(isinstance(basic, IComparable))   # True
print(isinstance(basic, IRentable))     # True

# Полиморфный вызов через интерфейсы
for apt in [basic, studio, luxury]:
    print(apt.to_string())              # IPrintable
    print(apt.get_rental_price())       # IRentable

# Сравнение через интерфейс
print(basic < luxury)                   # IComparable

# Работа с коллекцией через интерфейсы
collection = ApartmentCollection()
collection.add(basic)
collection.add(studio)
collection.add(luxury)

# Фильтрация по интерфейсам
printable = collection.get_printable()
comparable = collection.get_comparable()
rentable = collection.get_rentable()

# Универсальные функции
collection.print_all_items()
collection.calculate_total_rental_income()