"""
Модуль содержит иерархию классов для квартир.
На основе базового класса Apartment из ЛР-1 созданы производные классы:
- StudioApartment - квартира-студия
- LuxuryApartment - элитная квартира

Реализовано полиморфное поведение через метод calculate()
"""

from typing import List, Optional
from base import Apartment


class StudioApartment(Apartment):
    """
    Класс квартиры-студии.
    
    Наследуется от Apartment и добавляет специфичные атрибуты и методы.
    
    Дополнительные атрибуты:
        _has_kitchenette (bool): наличие кухонного уголка
        _studio_type (str): тип студии (стандарт, комфорт, премиум)
    
    Переопределённые методы:
        __str__() - расширенное представление
        calculate_monthly_payment() - расчёт с учётом типа студии
    """
    
    # Классификатор типов студий
    STUDIO_TYPES = ["стандарт", "комфорт", "премиум"]
    
    def __init__(self, area: float, price: float, address: str, rent_duration: int,
                 has_kitchenette: bool, studio_type: str):
        """
        Инициализация квартиры-студии.
        
        Args:
            area: площадь квартиры
            price: цена аренды
            address: адрес
            rent_duration: срок аренды в месяцах
            has_kitchenette: наличие кухонного уголка
            studio_type: тип студии (стандарт, комфорт, премиум)
        """
        # Вызов конструктора базового класса
        super().__init__(area, price, address, rent_duration)
        
        # Дополнительные атрибуты
        if not isinstance(has_kitchenette, bool):
            raise TypeError("has_kitchenette должен быть булевым значением")
        self._has_kitchenette = has_kitchenette
        
        if studio_type not in self.STUDIO_TYPES:
            raise ValueError(f"Тип студии должен быть одним из: {self.STUDIO_TYPES}")
        self._studio_type = studio_type
    
    # Геттеры для новых атрибутов
    @property
    def has_kitchenette(self) -> bool:
        return self._has_kitchenette
    
    @property
    def studio_type(self) -> str:
        return self._studio_type
    
    # Сеттеры для новых атрибутов
    @has_kitchenette.setter
    def has_kitchenette(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("has_kitchenette должен быть булевым значением")
        self._has_kitchenette = value
    
    @studio_type.setter
    def studio_type(self, value: str):
        if value not in self.STUDIO_TYPES:
            raise ValueError(f"Тип студии должен быть одним из: {self.STUDIO_TYPES}")
        self._studio_type = value
    
    # Переопределение метода базового класса
    def calculate_monthly_payment(self) -> float:
        """
        Расчёт ежемесячного платежа с учётом типа студии.
        
        Для студий премиум типа применяется повышающий коэффициент 1.2
        """
        base_payment = super().calculate_monthly_payment()
        
        # Повышающий коэффициент для премиум студий
        if self._studio_type == "премиум":
            return base_payment * 1.2
        elif self._studio_type == "комфорт":
            return base_payment * 1.1
        return base_payment
    
    # Переопределение метода __str__
    def __str__(self) -> str:
        """Расширенное представление квартиры-студии."""
        base_str = super().__str__()
        kitchen_info = "с кухонным уголком" if self._has_kitchenette else "без кухонного уголка"
        
        return (f"{base_str}\n"
                f"  Тип: Студия ({self._studio_type})\n"
                f"  Кухонный уголок: {kitchen_info}")
    
    # Переопределение __repr__
    def __repr__(self) -> str:
        return (f"StudioApartment(area={self._area}, price={self._price}, "
                f"address='{self._address}', rent_duration={self._rent_duration}, "
                f"has_kitchenette={self._has_kitchenette}, studio_type='{self._studio_type}')")
    
    # Новый метод, специфичный для студий
    def is_suitable_for_students(self) -> bool:
        """
        Проверка пригодности для студентов.
        
        Returns:
            bool: True если студия подходит для студентов
        """
        # Подходит если есть кухонный уголок и тип стандарт или комфорт
        return self._has_kitchenette and self._studio_type in ["стандарт", "комфорт"]


class LuxuryApartment(Apartment):
    """
    Класс элитной квартиры.
    
    Наследуется от Apartment и добавляет специфичные атрибуты и методы.
    
    Дополнительные атрибуты:
        _has_parking (bool): наличие парковочного места
        _floor_level (str): уровень этажа (низкий, средний, высокий, пентхаус)
        _luxury_features (List[str]): список элитных особенностей
    
    Переопределённые методы:
        __str__() - расширенное представление
        calculate_monthly_payment() - расчёт с учётом элитности
    """
    
    # Классификатор уровней этажей
    FLOOR_LEVELS = ["низкий", "средний", "высокий", "пентхаус"]
    
    def __init__(self, area: float, price: float, address: str, rent_duration: int,
                 has_parking: bool, floor_level: str, luxury_features: Optional[List[str]] = None):
        """
        Инициализация элитной квартиры.
        
        Args:
            area: площадь квартиры
            price: цена аренды
            address: адрес
            rent_duration: срок аренды в месяцах
            has_parking: наличие парковочного места
            floor_level: уровень этажа
            luxury_features: список элитных особенностей (по умолчанию пуст)
        """
        # Вызов конструктора базового класса
        super().__init__(area, price, address, rent_duration)
        
        # Дополнительные атрибуты
        if not isinstance(has_parking, bool):
            raise TypeError("has_parking должен быть булевым значением")
        self._has_parking = has_parking
        
        if floor_level not in self.FLOOR_LEVELS:
            raise ValueError(f"Уровень этажа должен быть одним из: {self.FLOOR_LEVELS}")
        self._floor_level = floor_level
        
        self._luxury_features = luxury_features if luxury_features else []
    
    # Геттеры для новых атрибутов
    @property
    def has_parking(self) -> bool:
        return self._has_parking
    
    @property
    def floor_level(self) -> str:
        return self._floor_level
    
    @property
    def luxury_features(self) -> List[str]:
        return self._luxury_features.copy()
    
    # Сеттеры для новых атрибутов
    @has_parking.setter
    def has_parking(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("has_parking должен быть булевым значением")
        self._has_parking = value
    
    @floor_level.setter
    def floor_level(self, value: str):
        if value not in self.FLOOR_LEVELS:
            raise ValueError(f"Уровень этажа должен быть одним из: {self.FLOOR_LEVELS}")
        self._floor_level = value
    
    def add_luxury_feature(self, feature: str) -> None:
        """
        Добавление элитной особенности.
        
        Args:
            feature: название особенности
        """
        if not isinstance(feature, str) or not feature.strip():
            raise ValueError("Особенность должна быть непустой строкой")
        
        feature = feature.strip()
        if feature not in self._luxury_features:
            self._luxury_features.append(feature)
    
    # Переопределение метода базового класса
    def calculate_monthly_payment(self) -> float:
        """
        Расчёт ежемесячного платежа с учётом элитности.
        
        Для элитных квартир применяются повышающие коэффициенты:
        - пентхаус: +50%
        - высокий этаж: +20%
        - наличие парковки: +10%
        """
        base_payment = super().calculate_monthly_payment()
        
        # Повышающие коэффициенты
        if self._floor_level == "пентхаус":
            base_payment *= 1.5
        elif self._floor_level == "высокий":
            base_payment *= 1.2
        
        if self._has_parking:
            base_payment *= 1.1
        
        # Дополнительная наценка за количество особенностей
        if len(self._luxury_features) > 3:
            base_payment *= 1.15
        
        return base_payment
    
    # Переопределение метода __str__
    def __str__(self) -> str:
        """Расширенное представление элитной квартиры."""
        base_str = super().__str__()
        parking_info = "с парковкой" if self._has_parking else "без парковки"
        features_str = ", ".join(self._luxury_features) if self._luxury_features else "нет особенностей"
        
        return (f"{base_str}\n"
                f"  Тип: Элитная квартира\n"
                f"  Этаж: {self._floor_level}\n"
                f"  Парковка: {parking_info}\n"
                f"  Особенности: {features_str}")
    
    # Переопределение __repr__
    def __repr__(self) -> str:
        return (f"LuxuryApartment(area={self._area}, price={self._price}, "
                f"address='{self._address}', rent_duration={self._rent_duration}, "
                f"has_parking={self._has_parking}, floor_level='{self._floor_level}', "
                f"luxury_features={self._luxury_features})")
    
    # Новый метод, специфичный для элитных квартир
    def is_vip(self) -> bool:
        """
        Проверка VIP статуса.
        
        Returns:
            bool: True если квартира имеет VIP статус
        """
        # VIP если пентхаус или есть более 3 особенностей
        return self._floor_level == "пентхаус" or len(self._luxury_features) > 3
    
    # Новый метод для проверки пригодности для семей
    def is_suitable_for_family(self) -> bool:
        """
        Проверка пригодности для семей.
        
        Returns:
            bool: True если квартира подходит для семей
        """
        # Подходит если есть парковка и площадь больше 60 м²
        return self._has_parking and self._area > 60