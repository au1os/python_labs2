"""
Модуль содержит стратегии и функции-обработчики для работы с квартирами.
Реализует паттерн "Стратегия" через callable-объекты и функции высшего порядка.
"""

from typing import Callable, List, Any
import sys
from pathlib import Path

# Добавляем путь к lab01 для импорта базового класса
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment


# ============================================================================
# Стратегии сортировки (функции-ключи для sorted/sort)
# ============================================================================

def by_price(apartment: Apartment) -> float:
    """
    Стратегия сортировки: по цене (возрастание).
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        float: Цена квартиры
    """
    return apartment.price


def by_price_desc(apartment: Apartment) -> float:
    """
    Стратегия сортировки: по цене (убывание).
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        float: Отрицательная цена (для сортировки по убыванию)
    """
    return -apartment.price


def by_area(apartment: Apartment) -> float:
    """
    Стратегия сортировки: по площади (возрастание).
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        float: Площадь квартиры
    """
    return apartment.area


def by_area_desc(apartment: Apartment) -> float:
    """
    Стратегия сортировки: по площади (убывание).
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        float: Отрицательная площадь (для сортировки по убыванию)
    """
    return -apartment.area


def by_rent_duration(apartment: Apartment) -> int:
    """
    Стратегия сортировки: по сроку аренды (возрастание).
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        int: Срок аренды в месяцах
    """
    return apartment.rent_duration


def by_monthly_payment(apartment: Apartment) -> float:
    """
    Стратегия сортировки: по ежемесячному платежу (возрастание).
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        float: Ежемесячный платёж
    """
    return apartment.calculate_monthly_payment()


def by_address(apartment: Apartment) -> str:
    """
    Стратегия сортировки: по адресу (алфавит).
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        str: Адрес квартиры
    """
    return apartment.address


# ============================================================================
# Функции-фильтры (предикаты)
# ============================================================================

def is_available(apartment: Apartment) -> bool:
    """
    Фильтр: проверка доступности квартиры (не арендована).
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        bool: True если квартира свободна
    """
    return not apartment.is_rented


def is_rented(apartment: Apartment) -> bool:
    """
    Фильтр: проверка, арендована ли квартира.
    
    Args:
        apartment: Объект квартиры
        
    Returns:
        bool: True если квартира арендована
    """
    return apartment.is_rented


def is_expensive(apartment: Apartment, threshold: float = 100000) -> bool:
    """
    Фильтр: проверка, дороже ли квартира заданного порога.
    
    Args:
        apartment: Объект квартиры
        threshold: Порог стоимости (по умолчанию 100000)
        
    Returns:
        bool: True если цена выше порога
    """
    return apartment.price > threshold


def is_large(apartment: Apartment, min_area: float = 60.0) -> bool:
    """
    Фильтр: проверка, является ли квартира большой (площадь >= min_area).
    
    Args:
        apartment: Объект квартиры
        min_area: Минимальная площадь (по умолчанию 60.0 м²)
        
    Returns:
        bool: True если площадь >= min_area
    """
    return apartment.area >= min_area


def is_small(apartment: Apartment, max_area: float = 40.0) -> bool:
    """
    Фильтр: проверка, является ли квартира маленькой (площадь <= max_area).
    
    Args:
        apartment: Объект квартиры
        max_area: Максимальная площадь (по умолчанию 40.0 м²)
        
    Returns:
        bool: True если площадь <= max_area
    """
    return apartment.area <= max_area


def is_in_budget(apartment: Apartment, max_price: float) -> bool:
    """
    Фильтр: проверка, входит ли квартира в бюджет.
    
    Args:
        apartment: Объект квартиры
        max_price: Максимальная цена
        
    Returns:
        bool: True if price <= max_price
    """
    return apartment.price <= max_price


def has_short_rent(apartment: Apartment, max_duration: int = 6) -> bool:
    """
    Фильтр: проверка, короткий ли срок аренды.
    
    Args:
        apartment: Объект квартиры
        max_duration: Максимальный срок аренды в месяцах (по умолчанию 6)
        
    Returns:
        bool: True if rent_duration <= max_duration
    """
    return apartment.rent_duration <= max_duration


# ============================================================================
# Фабрики функций (функции высшего порядка, возвращающие функции)
# ============================================================================

def make_price_filter(max_price: float) -> Callable[[Apartment], bool]:
    """
    Фабрика функций: создаёт фильтр по максимальной цене.
    
    Args:
        max_price: Максимальная допустимая цена
        
    Returns:
        Callable[[Apartment], bool]: Функция-фильтр
    """
    def filter_fn(apartment: Apartment) -> bool:
        return apartment.price <= max_price
    return filter_fn


def make_min_area_filter(min_area: float) -> Callable[[Apartment], bool]:
    """
    Фабрика функций: создаёт фильтр по минимальной площади.
    
    Args:
        min_area: Минимальная допустимая площадь
        
    Returns:
        Callable[[Apartment], bool]: Функция-фильтр
    """
    def filter_fn(apartment: Apartment) -> bool:
        return apartment.area >= min_area
    return filter_fn


def make_price_range_filter(min_price: float, max_price: float) -> Callable[[Apartment], bool]:
    """
    Фабрика функций: создаёт фильтр по диапазону цен.
    
    Args:
        min_price: Минимальная цена
        max_price: Максимальная цена
        
    Returns:
        Callable[[Apartment], bool]: Функция-фильтр
    """
    def filter_fn(apartment: Apartment) -> bool:
        return min_price <= apartment.price <= max_price
    return filter_fn


def make_discount_strategy(discount_percent: float) -> Callable[[Apartment], float]:
    """
    Фабрика функций: создаёт стратегию расчёта цены со скидкой.
    
    Args:
        discount_percent: Процент скидки (например, 10 для 10%)
        
    Returns:
        Callable[[Apartment], float]: Функция, возвращающая цену со скидкой
    """
    def discount_fn(apartment: Apartment) -> float:
        return apartment.price * (1 - discount_percent / 100)
    return discount_fn


# ============================================================================
# Стратегии обработки (callable-объекты)
# ============================================================================

class DiscountStrategy:
    """
    Стратегия применения скидки к цене квартиры.
    Реализует паттерн "Стратегия" через callable-объект.
    """
    
    def __init__(self, discount_percent: float):
        """
        Инициализация стратегии скидки.
        
        Args:
            discount_percent: Процент скидки (например, 10 для 10%)
        """
        self._discount_percent = discount_percent
    
    def __call__(self, item: Apartment) -> float:
        """
        Применение скидки к квартире.
        
        Args:
            item: Объект квартиры
            
        Returns:
            float: Цена со скидкой
        """
        return item.price * (1 - self._discount_percent / 100)
    
    def __repr__(self) -> str:
        return f"DiscountStrategy({self._discount_percent}%)"


class MonthlyPaymentStrategy:
    """
    Стратегия расчёта ежемесячного платежа.
    Реализует паттерн "Стратегия" через callable-объект.
    """
    
    def __call__(self, item: Apartment) -> float:
        """
        Расчёт ежемесячного платежа.
        
        Args:
            item: Объект квартиры
            
        Returns:
            float: Ежемесячный платёж
        """
        return item.calculate_monthly_payment()
    
    def __repr__(self) -> str:
        return "MonthlyPaymentStrategy()"


class PricePerSqmStrategy:
    """
    Стратегия расчёта цены за квадратный метр.
    Реализует паттерн "Стратегия" через callable-объект.
    """
    
    def __call__(self, item: Apartment) -> float:
        """
        Расчёт цены за квадратный метр.
        
        Args:
            item: Объект квартиры
            
        Returns:
            float: Цена за м²
        """
        return item.price / item.area
    
    def __repr__(self) -> str:
        return "PricePerSqmStrategy()"


class AddressFormatter:
    """
    Стратегия форматирования адреса.
    Реализует паттерн "Стратегия" через callable-объект.
    """
    
    def __init__(self, short: bool = False):
        """
        Инициализация форматтера.
        
        Args:
            short: Если True, возвращать короткий формат
        """
        self._short = short
    
    def __call__(self, item: Apartment) -> str:
        """
        Форматирование адреса.
        
        Args:
            item: Объект квартиры
            
        Returns:
            str: Форматированный адрес
        """
        if self._short:
            return item.address.split(',')[0]
        return item.address
    
    def __repr__(self) -> str:
        return f"AddressFormatter(short={self._short})"