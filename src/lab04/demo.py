"""
Демонстрация работы интерфейсов и абстрактных классов.
Сценарии использования:
1. Работа с интерфейсами IPrintable, IComparable, IRentable
2. Универсальные функции через интерфейсы
3. Фильтрация коллекции через интерфейсы
4. Полиморфизм без условий через интерфейсы
"""

from collection import ApartmentCollection
from interfaces import IPrintable, IComparable, IRentable
from models import ApartmentBase, StudioApartment, LuxuryApartment


def scenario_1_interface_usage():
    """
    Сценарий 1: Работа с интерфейсами IPrintable, IComparable, IRentable
    - Создание объектов разных типов
    - Проверка реализации интерфейсов через isinstance()
    - Вызов методов интерфейсов
    """
    print("=" * 60)
    print("СЦЕНАРИЙ 1: Работа с интерфейсами IPrintable, IComparable, IRentable")
    print("=" * 60)
    
    # Создание объектов
    print("\n1. Создание объектов разных типов:")
    basic = ApartmentBase(50.0, 100000, "ул. Примерная, д.1, кв.10", 12)
    studio = StudioApartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6, True, "комфорт")
    luxury = LuxuryApartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12, True, "пентхаус", ["вид на город", "терраса"])
    
    print(f"   Создана базовая квартира: {type(basic).__name__}")
    print(f"   Создана студия: {type(studio).__name__}")
    print(f"   Создана элитная квартира: {type(luxury).__name__}")
    
    # Проверка реализации интерфейсов
    print("\n2. Проверка реализации интерфейсов через isinstance():")
    for apt in [basic, studio, luxury]:
        print(f"   {type(apt).__name__}:")
        print(f"     IPrintable: {isinstance(apt, IPrintable)}")
        print(f"     IComparable: {isinstance(apt, IComparable)}")
        print(f"     IRentable: {isinstance(apt, IRentable)}")
    
    # Использование IPrintable
    print("\n3. Использование интерфейса IPrintable:")
    print("   Вызов to_string():")
    for apt in [basic, studio, luxury]:
        print(f"   {apt.to_string()[:50]}...")
    
    print("\n   Вызов print_info():")
    for apt in [basic, studio, luxury]:
        print(f"   --- {type(apt).__name__} ---")
        apt.print_info()
        print()
    
    # Использование IComparable
    print("\n4. Использование интерфейса IComparable:")
    print("   Сравнение объектов:")
    
    # Сравнение базовых квартир (по цене)
    basic2 = ApartmentBase(60.0, 120000, "ул. Центральная, d.20, кв.50", 6)
    print(f"   basic (100000) vs basic2 (120000): {basic.compare_to(basic2)}")
    print(f"   basic < basic2: {basic < basic2}")
    print(f"   basic > basic2: {basic > basic2}")
    
    # Сравнение студий (по площади)
    studio2 = StudioApartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6, True, "премиум")
    print(f"   studio (35 м²) vs studio2 (40 м²): {studio.compare_to(studio2)}")
    print(f"   studio < studio2: {studio < studio2}")
    
    # Сравнение элитных (по количеству особенностей)
    luxury2 = LuxuryApartment(80.0, 200000, "ул. Комфортная, д.15, кв.30", 12, False, "средний", ["консьерж", "бассейн", "сауна"])
    print(f"   luxury (2 особенности) vs luxury2 (3 особенности): {luxury.compare_to(luxury2)}")
    print(f"   luxury < luxury2: {luxury < luxury2}")
    
    # Использование IRentable
    print("\n5. Использование интерфейса IRentable:")
    for apt in [basic, studio, luxury]:
        print(f"   {type(apt).__name__}:")
        print(f"     get_rental_price(): {apt.get_rental_price():,.2f} руб./мес.")
        print(f"     is_available(): {apt.is_available()}")
    
    # Аренда и проверка доступности
    print("\n   Аренда студии:")
    studio.rent()
    print(f"   is_available() after rent: {studio.is_available()}")
    
    print("\n   Освобождение студии:")
    studio.vacate()
    print(f"   is_available() after vacate: {studio.is_available()}")
    
    print("\n" + "=" * 60)


def scenario_2_universal_functions():
    """
    Сценарий 2: Универсальные функции через интерфейсы
    - Работа функции, работающей с разными объектами через интерфейс
    - Полиморфизм без условий
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 2: Универсальные функции через интерфейсы")
    print("=" * 60)
    
    # Создание коллекции
    print("\n1. Создание коллекции с разными типами:")
    collection = ApartmentCollection()
    
    collection.add(ApartmentBase(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(StudioApartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6, True, "комфорт"))
    collection.add(LuxuryApartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12, True, "пентхаус", ["вид на город", "терраса"]))
    collection.add(ApartmentBase(60.0, 120000, "ул. Центральная, d.20, кв.50", 6))
    collection.add(StudioApartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6, True, "премиум"))
    
    print(f"   Добавлено {len(collection)} квартир")
    
    # Универсальная функция печати через интерфейс IPrintable
    print("\n2. Универсальная функция печати (через IPrintable):")
    print("   collection.print_all_items():")
    collection.print_all_items()
    
    # Универсальная функция сравнения через интерфейс IComparable
    print("\n3. Универсальная функция сравнения (через IComparable):")
    print("   collection.sort_by_comparison():")
    collection.sort_by_comparison()
    print("   После сортировки (по умолчанию - по цене):")
    for i, apt in enumerate(collection, 1):
        print(f"   {i}. {apt.address}: {apt.price:,.2f} руб.")
    
    # Универсальная функция расчёта дохода через интерфейс IRentable
    print("\n4. Универсальная функция расчёта дохода (через IRentable):")
    total_income = collection.calculate_total_rental_income()
    print(f"   collection.calculate_total_rental_income(): {total_income:,.2f} руб./мес.")
    
    # Получение доступных для аренды через интерфейс IRentable
    print("\n5. Получение доступных для аренды (через IRentable):")
    available = collection.get_available_rentals()
    print(f"   collection.get_available_rentals(): {len(available)} объектов")
    for apt in available:
        print(f"   - {apt.address}: {apt.get_rental_price():,.2f} руб./мес.")
    
    print("\n" + "=" * 60)


def scenario_3_interface_filtering():
    """
    Сценарий 3: Фильтрация коллекции через интерфейсы
    - Работа с коллекцией через интерфейсы
    - Фильтрация по типам интерфейсов
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 3: Фильтрация коллекции через интерфейсы")
    print("=" * 60)
    
    # Создание коллекции
    print("\n1. Создание коллекции:")
    collection = ApartmentCollection()
    
    collection.add(ApartmentBase(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(StudioApartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6, True, "комфорт"))
    collection.add(LuxuryApartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12, True, "пентхаус", ["вид на город"]))
    collection.add(ApartmentBase(60.0, 120000, "ул. Центральная, d.20, кв.50", 6))
    collection.add(StudioApartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6, True, "премиум"))
    collection.add(LuxuryApartment(80.0, 200000, "ул. Комфортная, д.15, кв.30", 12, False, "средний", ["консьерж"]))
    
    print(f"   Всего квартир: {len(collection)}")
    
    # Фильтрация по интерфейсу IPrintable
    print("\n2. Фильтрация по интерфейсу IPrintable:")
    printable = collection.get_printable()
    print(f"   collection.get_printable(): {len(printable)} объектов")
    print(f"   Все объекты реализуют IPrintable: {all(isinstance(apt, IPrintable) for apt in printable)}")
    
    # Фильтрация по интерфейсу IComparable
    print("\n3. Фильтрация по интерфейсу IComparable:")
    comparable = collection.get_comparable()
    print(f"   collection.get_comparable(): {len(comparable)} объектов")
    print(f"   Все объекты реализуют IComparable: {all(isinstance(apt, IComparable) for apt in comparable)}")
    
    # Фильтрация по интерфейсу IRentable
    print("\n4. Фильтрация по интерфейсу IRentable:")
    rentable = collection.get_rentable()
    print(f"   collection.get_rentable(): {len(rentable)} объектов")
    print(f"   Все объекты реализуют IRentable: {all(isinstance(apt, IRentable) for apt in rentable)}")
    
    # Комбинированная фильтрация (по типам и интерфейсам)
    print("\n5. Комбинированная фильтрация:")
    print("   Получаем только студии через интерфейс IFilterable:")
    studios = collection.filter_by(lambda x: isinstance(x, StudioApartment))
    print(f"   Найдено студий: {len(studios)}")
    for apt in studios:
        print(f"   - {apt.address}")
    
    print("\n   Получаем только элитные через интерфейс IFilterable:")
    luxury = collection.filter_by(lambda x: isinstance(x, LuxuryApartment))
    print(f"   Найдено элитных: {len(luxury)}")
    for apt in luxury:
        print(f"   - {apt.address}")
    
    print("\n   Получаем доступные квартиры через интерфейс IFilterable:")
    available = collection.filter_by(lambda x: x.is_available())
    print(f"   Найдено доступных: {len(available)}")
    for apt in available:
        print(f"   - {apt.address}")
    
    print("\n" + "=" * 60)


def scenario_4_polymorphism_without_conditions():
    """
    Сценарий 4: Полиморфизм без условий через интерфейсы
    - Единый список объектов разных типов
    - Вызов одинаковых методов через интерфейсы
    - Разное поведение у разных классов
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 4: Полиморфизм без условий через интерфейсы")
    print("=" * 60)
    
    # Создание смешанной коллекции
    print("\n1. Создание смешанной коллекции:")
    collection = ApartmentCollection()
    
    collection.add(ApartmentBase(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(StudioApartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6, True, "комфорт"))
    collection.add(LuxuryApartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12, True, "пентхаус", ["вид на город", "терраса"]))
    collection.add(ApartmentBase(60.0, 120000, "ул. Центральная, d.20, кв.50", 6))
    collection.add(StudioApartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6, True, "премиум"))
    
    print(f"   Добавлено {len(collection)} квартир")
    
    # Полиморфный вызов to_string() через интерфейс IPrintable
    print("\n2. Полиморфный вызов to_string() (через IPrintable):")
    print("   (один и тот же метод работает по-разному для разных типов)")
    for apt in collection:
        # Вызываем через интерфейс, без проверки типа
        print(f"   {type(apt).__name__}: {apt.to_string()[:60]}...")
    
    # Полиморфный вызов compare_to() через интерфейс IComparable
    print("\n3. Полиморфный вызов compare_to() (через IComparable):")
    print("   (разное поведение сравнения у разных типов)")
    
    # Сортировка через интерфейс
    collection.sort_by_comparison()
    print("   После сортировки (каждый тип сравнивается по-своему):")
    for i, apt in enumerate(collection, 1):
        print(f"   {i}. {type(apt).__name__}: {apt.address}")
    
    # Полиморфный вызов get_rental_price() через интерфейс IRentable
    print("\n4. Полиморфный вызов get_rental_price() (через IRentable):")
    print("   (разный расчёт цены у разных типов)")
    for apt in collection:
        # Вызываем через интерфейс, без проверки типа
        price = apt.get_rental_price()
        print(f"   {type(apt).__name__}: {price:,.2f} руб./мес.")
    
    # Демонстрация отсутствия условий (good pattern)
    print("\n5. Демонстрация правильного паттерна (без if type == ...):")
    print("   Вместо:")
    print("     if isinstance(obj, StudioApartment):")
    print("         ...")
    print("     elif isinstance(obj, LuxuryApartment):")
    print("         ...")
    print("   Используем:")
    print("     obj.to_string()  # Работает для всех типов через интерфейс")
    
    print("\n" + "=" * 60)


def main():
    """Основная функция, запускающая все сценарии."""
    print("*" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ИНТЕРФЕЙСОВ И АБСТРАКТНЫХ КЛАССОВ")
    print("Лабораторная работа №4 - Интерфейсы и абстрактные классы (ABC)")
    print("*" * 60)
    
    # Запуск всех сценариев
    scenario_1_interface_usage()
    scenario_2_universal_functions()
    scenario_3_interface_filtering()
    scenario_4_polymorphism_without_conditions()
    
    print("\n" + "*" * 60)
    print("ВСЕ СЦЕНАРИИ УСПЕШНО ВЫПОЛНЕНЫ!")
    print("*" * 60)


if __name__ == "__main__":
    main()