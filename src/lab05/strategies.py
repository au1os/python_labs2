"""
Модуль содержит стратегии и функции-обработчики для работы с квартирами.
Реализует паттерн "Стратегия" через callable-объекты и функции высшего порядка.
"""

from typing import Callable, List, Any
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
        float: Отрицательная цена квартиры для сортировки по убыванию
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
        float: Отрицательная площадь квартиры для сортировки по убыванию
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
        str: Адрес квартиры в нижнем регистре
    """
    return apartment.address.lower()


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


def is_expensive(apartment: Apartment, threshold: float) -> bool:
    """
    Фильтр: проверка, является ли квартира дорогой (дороже порога).
    
    Args:
        apartment: Объект квартиры
        threshold: Порог стоимости
        
    Returns:
        bool: True если цена квартиры выше порога
    """
    return apartment.price > threshold


def is_large(apartment: Apartment, min_area: float = 60.0) -> bool:
    """
    Фильтр: проверка, является ли квартира большой.
    
    Args:
        apartment: Объект квартиры
        min_area: Минимальная площадь для больших квартир
        
    Returns:
        bool: True если площадь квартиры больше или равна min_area
    """
    return apartment.area >= min_area


def is_small(apartment: Apartment, max_area: float = 40.0) -> bool:
    """
    Фильтр: проверка, является ли квартира маленькой.
    
    Args:
        apartment: Объект квартиры
        max_area: Максимальная площадь для маленьких квартир
        
    Returns:
        bool: True если площадь квартиры меньше или равна max_area
    """
    return apartment.area <= max_area


def is_in_budget(apartment: Apartment, max_price: float) -> bool:
    """
    Фильтр: проверка, входит ли квартира в бюджет.
    
    Args:
        apartment: Объект квартиры
        max_price: Максимальная цена
        
    Returns:
        bool: True если цена квартиры меньше или равна max_price
    """
    return apartment.price <= max_price


def has_short_rent(apartment: Apartment, max_duration: int = 6) -> bool:
    """
    Фильтр: проверка, является ли срок аренды коротким.
    
    Args:
        apartment: Объект квартиры
        max_duration: Максимальный срок для короткой аренды
        
    Returns:
        bool: True если срок аренды меньше или равен max_duration
    """
    return apartment.rent_duration <= max_duration


# ============================================================================
# Фабрики функций (функции высшего порядка)
# ============================================================================

def make_price_filter(max_price: float) -> Callable[[Apartment], bool]:
    """
    Фабрика функций: создаёт фильтр по максимальной цене.
    
    Args:
        max_price: Максимальная цена
        
    Returns:
        Callable[[Apartment], bool]: Функция-фильтр
    """
    def filter_func(apartment: Apartment) -> bool:
        return apartment.price <= max_price
    return filter_func


def make_min_area_filter(min_area: float) -> Callable[[Apartment], bool]:
    """
    Фабрика функций: создаёт фильтр по минимальной площади.
    
    Args:
        min_area: Минимальная площадь
        
    Returns:
        Callable[[Apartment], bool]: Функция-фильтр
    """
    def filter_func(apartment: Apartment) -> bool:
        return apartment.area >= min_area
    return filter_func


def make_price_range_filter(min_price: float, max_price: float) -> Callable[[Apartment], bool]:
    """
    Фабрика функций: создаёт фильтр по диапазону цен.
    
    Args:
        min_price: Минимальная цена
        max_price: Максимальная цена
        
    Returns:
        Callable[[Apartment], bool]: Функция-фильтр
    """
    def filter_func(apartment: Apartment) -> bool:
        return min_price <= apartment.price <= max_price
    return filter_func


def make_discount_strategy(discount_percent: float) -> Callable[[Apartment], float]:
    """
    Фабрика функций: создаёт стратегию расчёта цены со скидкой.
    
    Args:
        discount_percent: Процент скидки
        
    Returns:
        Callable[[Apartment], float]: Функция расчёта цены со скидкой
    """
    def discount_func(apartment: Apartment) -> float:
        return apartment.price * (1 - discount_percent / 100)
    return discount_func


# ============================================================================
# Callable-объекты (паттерн "Стратегия")
# ============================================================================

class DiscountStrategy:
    """
    Стратегия: применение скидки к цене квартиры.
    
    Атрибуты:
        discount_percent (float): Процент скидки
    """
    
    def __init__(self, discount_percent: float):
        """
        Инициализация стратегии скидки.
        
        Args:
            discount_percent: Процент скидки
        """
        self.discount_percent = discount_percent
    
    def __call__(self, apartment: Apartment) -> float:
        """
        Применение скидки к квартире.
        
        Args:
            apartment: Объект квартиры
            
        Returns:
            float: Цена со скидкой
        """
        return apartment.price * (1 - self.discount_percent / 100)
    
    def __str__(self) -> str:
        return f"DiscountStrategy({self.discount_percent}%)"


class MonthlyPaymentStrategy:
    """
    Стратегия: расчёт ежемесячного платежа.
    """
    
    def __call__(self, apartment: Apartment) -> float:
        """
        Расчёт ежемесячного платежа.
        
        Args:
            apartment: Объект квартиры
            
        Returns:
            float: Ежемесячный платёж
        """
        return apartment.calculate_monthly_payment()
    
    def __str__(self) -> str:
        return "MonthlyPaymentStrategy()"


class PricePerSqmStrategy:
    """
    Стратегия: расчёт цены за квадратный метр.
    """
    
    def __call__(self, apartment: Apartment) -> float:
        """
        Расчёт цены за квадратный метр.
        
        Args:
            apartment: Объект квартиры
            
        Returns:
            float: Цена за квадратный метр
        """
        return apartment.price / apartment.area
    
    def __str__(self) -> str:
        return "PricePerSqmStrategy()"


class AddressFormatter:
    """
    Стратегия: форматирование адреса.
    
    Атрибуты:
        short (bool): Если True, возвращает короткую версию адреса
    """
    
    def __init__(self, short: bool = False):
        """
        Инициализация форматтера адресов.
        
        Args:
            short: Если True, возвращает короткую версию адреса
        """
        self.short = short
    
    def __call__(self, apartment: Apartment) -> str:
        """
        Форматирование адреса.
        
        Args:
            apartment: Объект квартиры
            
        Returns:
            str: Форматированный адрес
        """
        if self.short:
            # Короткий формат: только улица
            parts = apartment.address.split(',')
            return parts[0].strip() if parts else apartment.address
        return apartment.address
    
    def __str__(self) -> str:
        return f"AddressFormatter(short={self.short})"