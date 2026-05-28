"""
Демонстрация работы с обобщёнными (generic) классами и протоколами.
Сценарии использования:
1. TypedCollection с объектами Apartment из иерархии ЛР-3
2. TypedCollection с разными ограничениями (Displayable, Scorable)
"""

from container import TypedCollection, DisplayableCollection, ScorableCollection, Displayable, Scorable
from typing import List
import sys
from pathlib import Path

# Добавляем путь к lab01 для импорта базового класса
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment


def scenario_1_typed_collection_with_apartments():
    """
    Сценарий 1: TypedCollection[D] с объектами Apartment.
    Показывает, что объекты попадают в коллекцию без наследования от Protocol,
    и что методы протокола вызываются корректно.
    """
    print("=" * 60)
    print("СЦЕНАРИЙ 1: TypedCollection с объектами Apartment")
    print("=" * 60)
    
    # Создание типизированной коллекции для Apartment
    print("\n1. Создание типизированной коллекции TypedCollection[Apartment]:")
    apartments: TypedCollection[Apartment] = TypedCollection()
    
    # Добавление объектов
    print("\n2. Добавление объектов Apartment:")
    apt1 = Apartment(50.0, 100000, "ул. Примерная, д.1, кв.10", 12)
    apt2 = Apartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6)
    apt3 = Apartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12)
    apt4 = Apartment(60.0, 120000, "ул. Центральная, д.20, кв.50", 6)
    apt5 = Apartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6)
    
    apartments.add(apt1)
    apartments.add(apt2)
    apartments.add(apt3)
    apartments.add(apt4)
    apartments.add(apt5)
    
    print(f"   Добавлено {len(apartments)} квартир")
    
    # Демонстрация валидации типов
    print("\n3. Демонстрация валидации типов:")
    print(f"   Тип коллекции: {type(apartments).__name__}")
    print(f"   Тип элементов: Apartment")
    
    # Получение всех элементов
    print("\n4. Получение всех элементов и вывод каждого:")
    all_apartments = apartments.get_all()
    for i, apt in enumerate(all_apartments, 1):
        print(f"   {i}. {apt.address}: {apt.area} м², {apt.price:,.2f} руб.")
    
    # Использование метода find()
    print("\n5. Использование метода find():")
    
    # Поиск элемента (найден)
    found = apartments.find(lambda x: x.price > 200000)
    if found:
        print(f"   Найдена квартира дороже 200000: {found.address}")
    else:
        print("   Не найдено")
    
    # Поиск элемента (не найден)
    not_found = apartments.find(lambda x: x.area > 200)
    if not_found:
        print(f"   Найдена квартира больше 200 м²: {not_found.address}")
    else:
        print("   Не найдено квартир больше 200 м²")
    
    # Использование метода filter()
    print("\n6. Использование метода filter():")
    expensive = apartments.filter(lambda x: x.price > 100000)
    print(f"   Квартиры дороже 100000 ({len(expensive)} шт.):")
    for apt in expensive:
        print(f"   - {apt.address}: {apt.price:,.2f} руб.")
    
    # Использование метода map() с разными функциями
    print("\n7. Использование метода map() с разными функциями:")
    
    # Преобразование в строки (имена)
    addresses: List[str] = apartments.map(lambda x: x.address)
    print(f"   map() -> List[str] (адреса):")
    for addr in addresses[:3]:
        print(f"   - {addr}")
    
    # Преобразование в числа (цены)
    prices: List[float] = apartments.map(lambda x: x.price)
    print(f"   map() -> List[float] (цены):")
    for price in prices[:3]:
        print(f"   - {price:,.2f} руб.")
    
    # Преобразование в булевы значения (дорогие?)
    is_expensive: List[bool] = apartments.map(lambda x: x.price > 100000)
    print(f"   map() -> List[bool] (дороже 100000?):")
    for i, expensive in enumerate(is_expensive, 1):
        print(f"   {i}. {expensive}")
    
    print("\n" + "=" * 60)


def scenario_2_protocol_based_collections():
    """
    Сценарий 2: TypedCollection[S] с разными ограничениями.
    Показывает, что один и тот же класс TypedCollection работает
    с разными ограничениями через Protocol.
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 2: Протоколы Displayable и Scorable")
    print("=" * 60)
    
    # Проверка, что Apartment реализует протокол Displayable
    print("\n1. Проверка протокола Displayable для Apartment:")
    apt = Apartment(50.0, 100000, "ул. Тестовая, 1", 12)
    print(f"   hasattr(apt, 'display'): {hasattr(apt, 'display')}")
    print(f"   hasattr(apt, '__str__'): {hasattr(apt, '__str__')}")
    
    # Apartment не реализует Scorable (нет метода score)
    print("\n2. Проверка протокола Scorable для Apartment:")
    print(f"   hasattr(apt, 'score'): {hasattr(apt, 'score')}")
    
    # Создание коллекции с использованием DisplayableCollection
    print("\n3. Создание DisplayableCollection:")
    displayable_items: DisplayableCollection = DisplayableCollection()
    
    # Добавляем Apartment (реализует Displayable через __str__)
    displayable_items.add(apt)
    displayable_items.add(Apartment(35.0, 70000, "ул. Студенческая, 5", 6))
    displayable_items.add(Apartment(120.0, 300000, "пр. Элитный, 1", 12))
    
    print(f"   Добавлено {len(displayable_items)} объектов")
    
    # Вывод всех элементов через display_all()
    print("\n4. Вывод всех элементов через display_all():")
    displayable_items.display_all()
    
    # Создание ScorableCollection с объектами, реализующими Scorable
    print("\n5. Создание ScorableCollection с объектами, реализующими Scorable:")
    
    # Создадим класс, реализующий Scorable
    class RatedApartment:
        """Квартира с рейтингом (реализует Scorable)."""
        
        def __init__(self, area: float, price: float, address: str, rating: float):
            self._area = area
            self._price = price
            self._address = address
            self._rating = rating
        
        def score(self) -> float:
            """Возвращает рейтинг квартиры."""
            return self._rating
        
        def __str__(self) -> str:
            return f"{self._address}: {self._area} м², {self._price:,.2f} руб., рейтинг {self._rating}"
    
    # Создаём коллекцию с объектами, реализующими Scorable
    scorable_items: ScorableCollection = ScorableCollection()
    
    rated1 = RatedApartment(50.0, 100000, "ул. Примерная, 1", 4.5)
    rated2 = RatedApartment(35.0, 70000, "ул. Студенческая, 5", 4.2)
    rated3 = RatedApartment(120.0, 300000, "пр. Элитный, 1", 4.8)
    rated4 = RatedApartment(60.0, 120000, "ул. Центральная, 20", 4.0)
    
    scorable_items.add(rated1)
    scorable_items.add(rated2)
    scorable_items.add(rated3)
    scorable_items.add(rated4)
    
    print(f"   Добавлено {len(scorable_items)} объектов")
    
    # Получение оценок
    print("\n6. Получение оценок через get_scores():")
    scores = scorable_items.get_scores()
    for i, score in enumerate(scores, 1):
        print(f"   {i}. Рейтинг: {score}")
    
    # Расчёт средней оценки
    print("\n7. Расчёт средней оценки через get_average_score():")
    avg_score = scorable_items.get_average_score()
    print(f"   Средняя оценка: {avg_score:.2f}")
    
    # Демонстрация, что один и тот же TypedCollection работает с разными ограничениями
    print("\n8. Демонстрация универсальности TypedCollection:")
    print("   - TypedCollection[Apartment] работает с квартирами")
    print("   - DisplayableCollection работает с объектами, имеющими display()")
    print("   - ScorableCollection работает с объектами, имеющими score()")
    print("   Все используют один и тот же базовый класс TypedCollection!")
    
    print("\n" + "=" * 60)


def main():
    """Основная функция, запускающая все сценарии."""
    print("*" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ С GENERICS И TYPING")
    print("Лабораторная работа №6 - Generics и typing")
    print("*" * 60)
    
    # Запуск всех сценариев
    scenario_1_typed_collection_with_apartments()
    scenario_2_protocol_based_collections()
    
    print("\n" + "*" * 60)
    print("ВСЕ СЦЕНАРИИ УСПЕШНО ВЫПОЛНЕНЫ!")
    print("*" * 60)


if __name__ == "__main__":
    main()