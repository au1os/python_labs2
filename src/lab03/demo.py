"""
Демонстрация работы иерархии классов Apartment.
Сценарии использования:
1. Создание и работа с разными типами квартир
2. Полиморфизм и переопределение методов
3. Фильтрация по типам в коллекции
4. Расчёт доходов и аналитика
"""

from collection import ApartmentCollection
from base import Apartment
from models import StudioApartment, LuxuryApartment


def scenario_1_different_apartment_types():
    """
    Сценарий 1: Создание и работа с разными типами квартир
    - Создание базовых квартир
    - Создание квартир-студий
    - Создание элитных квартир
    - Вывод информации о каждом типе
    """
    print("=" * 60)
    print("СЦЕНАРИЙ 1: Создание и работа с разными типами квартир")
    print("=" * 60)
    
    # Создание базовой квартиры
    print("\n1. Создание базовой квартиры:")
    basic_apt = Apartment(50.0, 100000, "ул. Примерная, д.1, кв.10", 12)
    print(f"   Тип: {type(basic_apt).__name__}")
    print(f"   {basic_apt}")
    
    # Создание квартиры-студии
    print("\n2. Создание квартиры-студии:")
    studio_apt = StudioApartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6,
                                 has_kitchenette=True, studio_type="комфорт")
    print(f"   Тип: {type(studio_apt).__name__}")
    print(f"   {studio_apt}")
    
    # Создание элитной квартиры
    print("\n3. Создание элитной квартиры:")
    luxury_apt = LuxuryApartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12,
                                has_parking=True, floor_level="пентхаус",
                                luxury_features=["вид на город", "терраса", "джакузи", "умный дом"])
    print(f"   Тип: {type(luxury_apt).__name__}")
    print(f"   {luxury_apt}")
    
    # Создание ещё одной студии
    print("\n4. Создание ещё одной студии (премиум):")
    premium_studio = StudioApartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6,
                                    has_kitchenette=True, studio_type="премиум")
    print(f"   {premium_studio}")
    
    # Создание ещё одной элитной квартиры
    print("\n5. Создание ещё одной элитной квартиры (средний этаж):")
    mid_luxury = LuxuryApartment(80.0, 200000, "ул. Комфортная, д.15, кв.30", 12,
                                has_parking=False, floor_level="средний",
                                luxury_features=["консьерж", "бассейн"])
    print(f"   {mid_luxury}")
    
    print("\n" + "=" * 60)


def scenario_2_polymorphism():
    """
    Сценарий 2: Полиморфизм и переопределение методов
    - Вызов одинаковых методов у разных типов
    - Разное поведение методов
    - Проверка типов через isinstance()
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 2: Полиморфизм и переопределение методов")
    print("=" * 60)
    
    # Создание коллекции с разными типами
    print("\n1. Создание коллекции с разными типами квартир:")
    collection = ApartmentCollection()
    
    collection.add(Apartment(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(StudioApartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6, True, "комфорт"))
    collection.add(LuxuryApartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12, True, "пентхаус", ["вид на город", "терраса"]))
    collection.add(StudioApartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6, True, "премиум"))
    collection.add(LuxuryApartment(80.0, 200000, "ул. Комфортная, д.15, кв.30", 12, False, "средний", ["консьерж"]))
    
    print(f"   Добавлено {len(collection)} квартир")
    
    # Полиморфный вызов метода calculate_monthly_payment()
    print("\n2. Полиморфный вызов calculate_monthly_payment():")
    print("   (один и тот же метод работает по-разному для разных типов)")
    for i, apt in enumerate(collection, 1):
        payment = apt.calculate_monthly_payment()
        print(f"   {i}. {type(apt).__name__}: {payment:,.2f} руб./мес.")
    
    # Проверка типов через isinstance()
    print("\n3. Проверка типов через isinstance():")
    for i, apt in enumerate(collection, 1):
        is_basic = isinstance(apt, Apartment) and not isinstance(apt, (StudioApartment, LuxuryApartment))
        is_studio = isinstance(apt, StudioApartment)
        is_luxury = isinstance(apt, LuxuryApartment)
        
        type_str = []
        if is_basic: type_str.append("базовая")
        if is_studio: type_str.append("студия")
        if is_luxury: type_str.append("элитная")
        
        print(f"   {i}. {apt.address}: {', '.join(type_str)}")
    
    # Переопределение метода __str__()
    print("\n4. Переопределение метода __str__():")
    print("   (разное представление для разных типов)")
    for apt in collection:
        print(f"   {apt}")
        print()
    
    # Использование специфичных методов
    print("\n5. Использование специфичных методов:")
    for apt in collection:
        if isinstance(apt, StudioApartment):
            print(f"   Студия {apt.address}: подходит для студентов? {apt.is_suitable_for_students()}")
        elif isinstance(apt, LuxuryApartment):
            print(f"   Элитная {apt.address}: VIP? {apt.is_vip()}, подходит для семьи? {apt.is_suitable_for_family()}")
    
    print("\n" + "=" * 60)


def scenario_3_filtering_by_type():
    """
    Сценарий 3: Фильтрация по типам в коллекции
    - Получение только студий
    - Получение только элитных квартир
    - Получение только базовых квартир
    - Подсчёт количества по типам
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 3: Фильтрация по типам в коллекции")
    print("=" * 60)
    
    # Создание смешанной коллекции
    print("\n1. Создание смешанной коллекции:")
    collection = ApartmentCollection()
    
    collection.add(Apartment(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(StudioApartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6, True, "комфорт"))
    collection.add(LuxuryApartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12, True, "пентхаус", ["вид на город"]))
    collection.add(Apartment(60.0, 120000, "ул. Центральная, д.20, кв.50", 6))
    collection.add(StudioApartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6, True, "премиум"))
    collection.add(LuxuryApartment(80.0, 200000, "ул. Комфортная, д.15, кв.30", 12, False, "средний", ["консьерж"]))
    
    print(f"   Всего квартир: {len(collection)}")
    
    # Подсчёт по типам
    print("\n2. Подсчёт количества квартир по типам:")
    counts = collection.count_by_type()
    print(f"   Базовых: {counts['basic']}")
    print(f"   Студий: {counts['studio']}")
    print(f"   Элитных: {counts['luxury']}")
    
    # Получение только студий
    print("\n3. Получение только студий:")
    studios = collection.get_only_studios()
    print(f"   Найдено студий: {len(studios)}")
    for studio in studios:
        print(f"   - {studio.address} ({studio.studio_type})")
    
    # Получение только элитных квартир
    print("\n4. Получение только элитных квартир:")
    luxury = collection.get_only_luxury()
    print(f"   Найдено элитных: {len(luxury)}")
    for apt in luxury:
        print(f"   - {apt.address} ({apt.floor_level})")
    
    # Получение только базовых квартир
    print("\n5. Получение только базовых квартир:")
    basic = collection.get_only_basic()
    print(f"   Найдено базовых: {len(basic)}")
    for apt in basic:
        print(f"   - {apt.address}")
    
    # Универсальная фильтрация по типу
    print("\n6. Универсальная фильтрация через get_by_type():")
    print("   Получаем только студии:")
    studios_via_get = collection.get_by_type(StudioApartment)
    print(f"   Найдено: {len(studios_via_get)}")
    
    print("   Получаем только элитные:")
    luxury_via_get = collection.get_by_type(LuxuryApartment)
    print(f"   Найдено: {len(luxury_via_get)}")
    
    print("\n" + "=" * 60)


def scenario_4_income_analysis():
    """
    Сценарий 4: Расчёт доходов и аналитика
    - Аренда некоторых квартир
    - Расчёт общего месячного дохода
    - Комбинированная фильтрация и аналитика
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 4: Расчёт доходов и аналитика")
    print("=" * 60)
    
    # Создание коллекции
    print("\n1. Создание коллекции:")
    collection = ApartmentCollection()
    
    collection.add(Apartment(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(StudioApartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6, True, "комфорт"))
    collection.add(LuxuryApartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12, True, "пентхаус", ["вид на город", "терраса"]))
    collection.add(Apartment(60.0, 120000, "ул. Центральная, д.20, кв.50", 6))
    collection.add(StudioApartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6, True, "премиум"))
    
    print(f"   Добавлено {len(collection)} квартир")
    
    # Аренда некоторых квартир
    print("\n2. Аренда некоторых квартир:")
    collection[0].rent()  # Базовая
    collection[2].rent()  # Элитная
    print(f"   Арендованы: {collection[0].address} и {collection[2].address}")
    
    # Расчёт общего месячного дохода
    print("\n3. Расчёт общего месячного дохода от свободных квартир:")
    total_income = collection.calculate_total_monthly_income()
    print(f"   Общий месячный доход: {total_income:,.2f} руб.")
    
    # Детализация по типам
    print("\n4. Детализация дохода по типам квартир:")
    studios = collection.get_only_studios().get_available()
    luxury = collection.get_only_luxury().get_available()
    basic = collection.get_only_basic().get_available()
    
    studios_income = sum(apt.calculate_monthly_payment() for apt in studios)
    luxury_income = sum(apt.calculate_monthly_payment() for apt in luxury)
    basic_income = sum(apt.calculate_monthly_payment() for apt in basic)
    
    print(f"   Студии: {studios_income:,.2f} руб. ({len(studios)} шт.)")
    print(f"   Элитные: {luxury_income:,.2f} руб. ({len(luxury)} шт.)")
    print(f"   Базовые: {basic_income:,.2f} руб. ({len(basic)} шт.)")
    
    # Комбинированная фильтрация
    print("\n5. Комбинированная фильтрация (свободные студии + элитные):")
    available_studios_and_luxury = ApartmentCollection()
    for apt in collection:
        if (isinstance(apt, StudioApartment) or isinstance(apt, LuxuryApartment)) and not apt.is_rented:
            available_studios_and_luxury.add(apt)
    
    print(f"   Найдено: {len(available_studios_and_luxury)}")
    for apt in available_studios_and_luxury:
        print(f"   - {apt.address} ({type(apt).__name__})")
    
    # Сортировка по цене и вывод
    print("\n6. Сортировка всех свободных квартир по цене (по убыванию):")
    available = collection.get_available()
    available.sort_by_price(reverse=True)
    print(f"   Свободных квартир: {len(available)}")
    for i, apt in enumerate(available, 1):
        print(f"   {i}. {apt.address}: {apt.calculate_monthly_payment():,.2f} руб./мес.")
    
    print("\n" + "=" * 60)


def main():
    """Основная функция, запускающая все сценарии."""
    print("*" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ИЕРАРХИИ КЛАССОВ APARTMENT")
    print("Лабораторная работа №3 - Наследование и иерархия классов")
    print("*" * 60)
    
    # Запуск всех сценариев
    scenario_1_different_apartment_types()
    scenario_2_polymorphism()
    scenario_3_filtering_by_type()
    scenario_4_income_analysis()
    
    print("\n" + "*" * 60)
    print("ВСЕ СЦЕНАРИИ УСПЕШНО ВЫПОЛНЕНЫ!")
    print("*" * 60)


if __name__ == "__main__":
    main()