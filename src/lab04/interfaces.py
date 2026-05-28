"""
Модуль содержит абстрактные базовые классы (интерфейсы) для системы управления квартирами.
Реализует требования лабораторной работы №4:
- Минимум 2 интерфейса
- В каждом интерфейсе минимум 1 абстрактный метод
- Интерфейсы задают контракты поведения для классов
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class IPrintable(ABC):
    """
    Интерфейс для объектов, которые могут быть представлены в виде строки.
    
    Контракт: класс должен реализовать метод to_string(), который возвращает
    строковое представление объекта.
    """
    
    @abstractmethod
    def to_string(self) -> str:
        """
        Возвращает строковое представление объекта.
        
        Returns:
            str: Строковое представление объекта
        """
        pass
    
    def print_info(self) -> None:
        """
        Выводит информацию об объекте в консоль.
        Использует метод to_string().
        """
        print(self.to_string())


class IComparable(ABC):
    """
    Интерфейс для объектов, которые можно сравнивать между собой.
    
    Контракт: класс должен реализовать метод compare_to(other), который сравнивает
    текущий объект с другим объектом того же типа.
    """
    
    @abstractmethod
    def compare_to(self, other: 'IComparable') -> int:
        """
        Сравнивает текущий объект с другим объектом.
        
        Args:
            other (IComparable): Объект для сравнения
            
        Returns:
            int: отрицательное число, если текущий объект "меньше" other
                 0, если объекты "равны"
                 положительное число, если текущий объект "больше" other
        """
        pass
    
    def __lt__(self, other: 'IComparable') -> bool:
        """Оператор меньше (<) на основе compare_to()."""
        return self.compare_to(other) < 0
    
    def __le__(self, other: 'IComparable') -> bool:
        """Оператор меньше или равно (<=) на основе compare_to()."""
        return self.compare_to(other) <= 0
    
    def __gt__(self, other: 'IComparable') -> bool:
        """Оператор больше (>) на основе compare_to()."""
        return self.compare_to(other) > 0
    
    def __ge__(self, other: 'IComparable') -> bool:
        """Оператор больше или равно (>=) на основе compare_to()."""
        return self.compare_to(other) >= 0
    
    def __eq__(self, other: 'IComparable') -> bool:
        """Оператор равенства (==) на основе compare_to()."""
        return self.compare_to(other) == 0


class IRentable(ABC):
    """
    Интерфейс for объектов, которые можно сдавать в аренду.
    
    Контракт: класс должен реализовать методы для управления арендой.
    """
    
    @abstractmethod
    def get_rental_price(self) -> float:
        """
        Возвращает цену аренды.
        
        Returns:
            float: Цена аренды
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Проверяет доступность объекта для аренды.
        
        Returns:
            bool: True если объект доступен, False иначе
        """
        pass
    
    @abstractmethod
    def rent(self) -> None:
        """
        Сдаёт объект в аренду.
        
        Raises:
            RuntimeError: Если объект уже арендован
        """
        pass
    
    @abstractmethod
    def vacate(self) -> None:
        """
        Освобождает объект (прекращает аренду).
        
        Raises:
            RuntimeError: Если объект не арендован
        """
        pass


class IFilterable(ABC):
    """
    Интерфейс для коллекций, которые поддерживают фильтрацию.
    
    Контракт: коллекция должна уметь фильтровать свои элементы по заданному критерию.
    """
    
    @abstractmethod
    def filter_by(self, predicate) -> 'IFilterable':
        """
        Фильтрует элементы коллекции по заданному предикату.
        
        Args:
            predicate: Функция, принимающая элемент и возвращающая bool
            
        Returns:
            IFilterable: Новая коллекция с отфильтрованными элементами
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List:
        """
        Возвращает список всех элементов коллекции.
        
        Returns:
            List: Список элементов
        """
        pass