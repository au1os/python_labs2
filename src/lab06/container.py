"""
Модуль содержит обобщённый (generic) класс TypedCollection с поддержкой
системы аннотаций типов в Python (typing), включая Generic, TypeVar, Protocol.
"""

from typing import TypeVar, Generic, List, Iterator, Optional, Callable, Any
from typing import Protocol, runtime_checkable
import sys
from pathlib import Path

# Добавляем путь к lab01 для импорта базового класса
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment


# ============================================================================
# TypeVar для Generic-класса
# ============================================================================

T = TypeVar('T')
R = TypeVar('R')


# ============================================================================
# Protocol (структурная типизация)
# ============================================================================

@runtime_checkable
class Displayable(Protocol):
    """
    Протокол для объектов, которые могут быть отображены (имеют метод __str__).
    Классы не должны явно наследоваться от этого протокола — достаточно,
    что у них есть соответствующий метод.
    """
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта.
        
        Returns:
            str: Строковое представление
        """
        ...


@runtime_checkable
class Scorable(Protocol):
    """
    Протокол для объектов, которые могут быть оценены (имеют метод score).
    Классы не должны явно наследоваться от этого протокола — достаточно,
    что у них есть соответствующий метод.
    """
    
    def score(self) -> float:
        """
        Возвращает числовую оценку объекта.
        
        Returns:
            float: Оценка объекта
        """
        ...


# ============================================================================
# TypeVar с ограничениями (bound)
# ============================================================================

D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)


# ============================================================================
# Generic-класс TypedCollection
# ============================================================================

class TypedCollection(Generic[T]):
    """
    Обобщённый контейнерный класс для хранения и управления коллекцией объектов.
    Использует Generic для типизации хранимых элементов.
    
    Атрибуты:
        _items (List[T]): Внутренний список для хранения объектов типа T
    """
    
    def __init__(self) -> None:
        """Инициализирует пустую коллекцию."""
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        """
        Добавляет объект в коллекцию.
        
        Args:
            item (T): Объект для добавления
        """
        self._items.append(item)
    
    def remove(self, item: T) -> None:
        """
        Удаляет объект из коллекции.
        
        Args:
            item (T): Объект для удаления
            
        Raises:
            ValueError: Если объект не найден
        """
        self._items.remove(item)
    
    def get_all(self) -> List[T]:
        """
        Возвращает список всех объектов в коллекции.
        
        Returns:
            List[T]: Копия списка всех объектов
        """
        return self._items.copy()
    
    def get_at(self, index: int) -> T:
        """
        Возвращает объект по индексу.
        
        Args:
            index (int): Индекс объекта
            
        Returns:
            T: Объект по заданному индексу
        """
        return self._items[index]
    
    # ========================================================================
    # Методы с аннотациями типов (задание на 4)
    # ========================================================================
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Находит первый элемент, удовлетворяющий предикату.
        
        Args:
            predicate (Callable[[T], bool]): Функция-условие
            
        Returns:
            Optional[T]: Найденный элемент или None
        """
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Фильтрует элементы коллекции по заданному предикату.
        
        Args:
            predicate (Callable[[T], bool]): Функция-условие
            
        Returns:
            List[T]: Список всех подходящих элементов
        """
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        """
        Преобразует каждый элемент коллекции с помощью функции.
        Тип результата может быть другим — для этого нужен второй TypeVar R.
        
        Args:
            transform (Callable[[T], R]): Функция преобразования
            
        Returns:
            List[R]: Список результатов преобразования
        """
        return [transform(item) for item in self._items]
    
    # ========================================================================
    # Методы для работы с Protocol (задание на 5)
    # ========================================================================
    
    def display_all(self) -> None:
        """
        Выводит информацию обо всех объектах коллекции.
        Работает только с объектами, реализующими протокол Displayable.
        """
        for item in self._items:
            if isinstance(item, Displayable):
                print(item)
    
    def get_scores(self) -> List[float]:
        """
        Возвращает список оценок всех объектов.
        Работает только с объектами, реализующими протокол Scorable.
        
        Returns:
            List[float]: Список оценок
        """
        scores = []
        for item in self._items:
            if isinstance(item, Scorable):
                scores.append(item.score())
        return scores
    
    # ========================================================================
    # Магические методы
    # ========================================================================
    
    def __len__(self) -> int:
        """Возвращает количество объектов в коллекции."""
        return len(self._items)
    
    def __iter__(self) -> Iterator[T]:
        """Возвращает итератор по коллекции."""
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        """Возвращает объект по индексу."""
        return self._items[index]
    
    def __str__(self) -> str:
        """Возвращает строковое представление коллекции."""
        if not self._items:
            return f"{self.__class__.__name__} пуста (0 объектов)"
        
        result = f"{self.__class__.__name__} ({len(self._items)} объектов):\n"
        for i, item in enumerate(self._items, 1):
            result += f"  {i}. {item}\n"
        return result.strip()
    
    def __repr__(self) -> str:
        """Возвращает техническое представление коллекции."""
        return f"{self.__class__.__name__}(items={len(self._items)})"


# ============================================================================
# Специализированные коллекции с ограничениями
# ============================================================================

class DisplayableCollection(TypedCollection[D]):
    """
    Коллекция, которая может хранить только объекты, реализующие протокол Displayable.
    """
    
    def display_all(self) -> None:
        """Выводит информацию обо всех объектах коллекции."""
        for item in self._items:
            print(item)


class ScorableCollection(TypedCollection[S]):
    """
    Коллекция, которая может хранить только объекты, реализующие протокол Scorable.
    """
    
    def get_average_score(self) -> float:
        """
        Возвращает среднюю оценку всех объектов.
        
        Returns:
            float: Средняя оценка
        """
        if not self._items:
            return 0.0
        return sum(item.score() for item in self._items) / len(self._items)