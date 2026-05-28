"""
Демонстрация работы коллекции ApartmentCollection.
Сценарии использования:
1. Базовые операции с коллекцией (добавление, удаление, вывод)
2. Поиск и фильтрация квартир
3. Сортировка и продвинутые операции
4. Обработка ошибок и граничных случаев
"""

from collection import ApartmentCollection
from model import Apartment


def scenario_1_basic_operations():
    """
    Сценарий 1: Базовые операции с коллекцией
    - Создание коллекции
    - Добавление объектов
    - Вывод всех элементов
    - Удаление элемента
    - Проверка ограничений на дубликаты
    """
    print("=" * 60)
    print("СЦЕНАРИЙ 1: Базовые операции с коллекцией")
    print("=" * 60)
    
    # Создание коллекции
    print("\n1. Создание пустой коллекции:")
    collection = ApartmentCollection()
    print(f"   Коллекция создана: {repr(collection)}")
    print(f"   Количество квартир: {len(collection)}")
    
    # Создание объектов Apartment
    print("\n2. Создание нескольких объектов Apartment:")
    apt1 = Apartment(45.5, 75000, "ул. Ленина, д.10, кв.5", 12)
    apt2 = Apartment(62.0, 120000, "пр. Мира, д.25, кв.18", 6)
    apt3 = Apartment(30.0, 50000, "ул. Пушкина, д.1, кв.10", 12)
    print(f"   Создана квартира 1: {apt1.address}, {apt1.area} м²")
    print(f"   Создана квартира 2: {apt2.address}, {apt2.area} м²")
    print(f"   Создана квартира 3: {apt3.address}, {apt3.area} м²")
    
    # Добавление объектов в коллекцию
    print("\n3. Добавление объектов в коллекцию:")
    collection.add(apt1)
    collection.add(apt2)
    collection.add(apt3)
    print(f"   Добавлено 3 квартиры")
    print(f"   Количество квартир в коллекции: {len(collection)}")
    
    # Вывод всех элементов
    print("\n4. Вывод всех элементов коллекции:")
    print(collection)
    
    # Итерация по коллекции
    print("\n5. Итерация по коллекции (for item in collection):")
    for i, apartment in enumerate(collection, 1):
        print(f"   {i}. {apartment.address} - {apartment.area} м², {apartment.price:,.2f} руб.")
    
    # Удаление элемента
    print("\n6. Удаление элемента (apt2):")
    collection.remove(apt2)
    print(f"   Удалена квартира: {apt2.address}")
    print(f"   Количество квартир после удаления: {len(collection)}")
    print("   Оставшиеся квартиры:")
    for apartment in collection:
        print(f"   - {apartment.address}")
    
    # Проверка ограничений на дубликаты
    print("\n7. Проверка ограничения на дубликаты:")
    duplicate_apt = Apartment(45.5, 80000, "ул. Ленина, д.10, кв.5", 10)  # Такой же адрес и площадь
    try:
        collection.add(duplicate_apt)
        print("   ОШИБКА: Дубликат должен был быть отклонён!")
    except ValueError as e:
        print(f"   ✓ Дубликат отклонён: {e}")
    
    # Проверка типа добавляемых объектов
    print("\n8. Проверка типа добавляемых объектов:")
    try:
        collection.add("Не квартира")
        print("   ОШИБКА: Некорректный тип должен был быть отклонён!")
    except TypeError as e:
        print(f"   ✓ Некорректный тип отклонён: {e}")
    
    print("\n" + "=" * 60)


def scenario_2_search_and_filter():
    """
    Сценарий 2: Поиск и фильтрация квартир
    - Поиск по адресу
    - Фильтрация по цене
    - Фильтрация по площади
    - Получение свободных/арендованных квартир
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 2: Поиск и фильтрация квартир")
    print("=" * 60)
    
    # Создание коллекции с разными квартирами
    print("\n1. Создание коллекции с разными квартирами:")
    collection = ApartmentCollection()
    
    apartments = [
        Apartment(45.5, 75000, "ул. Ленина, д.10, кв.5", 12),
        Apartment(62.0, 120000, "пр. Мира, д.25, кв.18", 6),
        Apartment(30.0, 50000, "ул. Пушкина, д.1, кв.10", 12),
        Apartment(80.0, 150000, "ул. Гагарина, д.3, кв.42", 12),
        Apartment(55.0, 95000, "пр. Ленина, д.50, кв.8", 6),
    ]
    
    for apt in apartments:
        collection.add(apt)
    
    print(f"   Добавлено {len(collection)} квартир")
    
    # Аренда некоторых квартир для демонстрации фильтрации
    print("\n2. Аренда некоторых квартир:")
    collection[0].rent()  # ул. Ленина
    collection[2].rent()  # ул. Пушкина
    print(f"   Арендованы: {collection[0].address} и {collection[2].address}")
    
    # Поиск по адресу
    print("\n3. Поиск квартиры по адресу (полное совпадение):")
    found = collection.find_by_address("пр. Мира")
    if found:
        print(f"   ✓ Найдена: {found.address}, {found.area} м², {found.price:,.2f} руб.")
    else:
        print("   ✗ Не найдена")
    
    print("\n4. Поиск квартиры по адресу (частичное совпадение):")
    found = collection.find_by_address("Ленина")
    if found:
        print(f"   ✓ Найдена: {found.address}, {found.area} м²")
    else:
        print("   ✗ Не найдена")
    
    # Фильтрация по цене
    print("\n5. Фильтрация по цене (от 80000 до 130000 руб):")
    expensive_apts = collection.find_by_price_range(80000, 130000)
    print(f"   Найдено квартир: {len(expensive_apts)}")
    for apt in expensive_apts:
        print(f"   - {apt.address}: {apt.price:,.2f} руб.")
    
    # Фильтрация по площади
    print("\n6. Фильтрация по площади (от 50 до 70 м²):")
    medium_apts = collection.find_by_area_range(50, 70)
    print(f"   Найдено квартир: {len(medium_apts)}")
    for apt in medium_apts:
        print(f"   - {apt.address}: {apt.area} м²")
    
    # Получение свободных квартир
    print("\n7. Получение свободных квартир:")
    available = collection.get_available()
    print(f"   Свободных квартир: {len(available)}")
    for apt in available:
        print(f"   - {apt.address} ({'Свободна' if not apt.is_rented else 'Арендована'})")
    
    # Получение арендованных квартир
    print("\n8. Получение арендованных квартир:")
    rented = collection.get_rented()
    print(f"   Арендованных квартир: {len(rented)}")
    for apt in rented:
        print(f"   - {apt.address}")
    
    # Получение дорогих квартир
    print("\n9. Получение дорогих квартир (дороже 100000 руб):")
    expensive = collection.get_expensive(100000)
    print(f"   Дорогих квартир: {len(expensive)}")
    for apt in expensive:
        print(f"   - {apt.address}: {apt.price:,.2f} руб.")
    
    print("\n" + "=" * 60)


def scenario_3_sorting_and_indexing():
    """
    Сценарий 3: Сортировка и индексация
    - Индексация коллекции
    - Удаление по индексу
    - Сортировка по разным критериям
    - Универсальная сортировка
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 3: Сортировка и индексация")
    print("=" * 60)
    
    # Создание коллекции
    print("\n1. Создание коллекции:")
    collection = ApartmentCollection()
    
    apartments = [
        Apartment(45.5, 75000, "ул. Ленина, д.10, кв.5", 12),
        Apartment(62.0, 120000, "пр. Мира, д.25, кв.18", 6),
        Apartment(30.0, 50000, "ул. Пушкина, д.1, кв.10", 12),
        Apartment(80.0, 150000, "ул. Гагарина, д.3, кв.42", 12),
        Apartment(55.0, 95000, "пр. Ленина, д.50, кв.8", 6),
    ]
    
    for apt in apartments:
        collection.add(apt)
    
    print(f"   Добавлено {len(collection)} квартир")
    
    # Индексация
    print("\n2. Индексация коллекции (collection[0], collection[2]):")
    print(f"   collection[0]: {collection[0].address}, {collection[0].area} м²")
    print(f"   collection[2]: {collection[2].address}, {collection[2].area} м²")
    print(f"   collection[-1]: {collection[-1].address}, {collection[-1].area} м²")
    
    # Удаление по индексу
    print("\n3. Удаление по индексу (remove_at(1)):")
    removed = collection.remove_at(1)
    print(f"   Удалена: {removed.address}, {removed.area} м²")
    print(f"   Осталось квартир: {len(collection)}")
    
    # Сортировка по цене (по возрастанию)
    print("\n4. Сортировка по цене (по возрастанию):")
    collection.sort_by_price(reverse=False)
    print("   После сортировки:")
    for i, apt in enumerate(collection, 1):
        print(f"   {i}. {apt.address}: {apt.price:,.2f} руб.")
    
    # Сортировка по цене (по убыванию)
    print("\n5. Сортировка по цене (по убыванию):")
    collection.sort_by_price(reverse=True)
    print("   После сортировки:")
    for i, apt in enumerate(collection, 1):
        print(f"   {i}. {apt.address}: {apt.price:,.2f} руб.")
    
    # Сортировка по площади
    print("\n6. Сортировка по площади (по возрастанию):")
    collection.sort_by_area(reverse=False)
    print("   После сортировки:")
    for i, apt in enumerate(collection, 1):
        print(f"   {i}. {apt.address}: {apt.area} м²")
    
    # Универсальная сортировка
    print("\n7. Универсальная сортировка (по сроку аренды):")
    collection.sort(key=lambda x: x.rent_duration, reverse=True)
    print("   После сортировки по сроку аренды (по убыванию):")
    for i, apt in enumerate(collection, 1):
        print(f"   {i}. {apt.address}: {apt.rent_duration} мес.")
    
    # Комбинированная фильтрация и сортировка
    print("\n8. Комбинированная операция (фильтрация + сортировка):")
    print("   Получаем свободные квартиры и сортируем по цене:")
    available = collection.get_available()
    available.sort_by_price(reverse=True)
    print(f"   Свободных квартир: {len(available)}")
    for i, apt in enumerate(available, 1):
        status = "Арендована" if apt.is_rented else "Свободна"
        print(f"   {i}. {apt.address}: {apt.price:,.2f} руб. ({status})")
    
    print("\n" + "=" * 60)


def scenario_4_edge_cases():
    """
    Сценарий 4: Обработка ошибок и граничных случаев
    - Пустая коллекция
    - Некорректные индексы
    - Удаление несуществующего элемента
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 4: Обработка ошибок и граничных случаев")
    print("=" * 60)
    
    # Пустая коллекция
    print("\n1. Работа с пустой коллекцией:")
    empty_collection = ApartmentCollection()
    print(f"   Пустая коллекция: {empty_collection}")
    print(f"   Длина: {len(empty_collection)}")
    
    # Попытка удаления из пустой коллекции
    print("\n2. Попытка удаления несуществующего элемента:")
    try:
        fake_apt = Apartment(50, 100000, "ул. Тестовая, 1", 12)
        empty_collection.remove(fake_apt)
        print("   ОШИБКА: Должно было выбросить исключение!")
    except ValueError as e:
        print(f"   ✓ Исключение обработано: {e}")
    
    # Некорректные индексы
    print("\n3. Некорректные индексы:")
    collection = ApartmentCollection()
    collection.add(Apartment(50, 100000, "ул. Тестовая, 1", 12))
    
    try:
        collection[10]
        print("   ОШИБКА: Должно было выбросить IndexError!")
    except IndexError as e:
        print(f"   ✓ IndexError при доступе: {e}")
    
    try:
        collection.remove_at(5)
        print("   ОШИБКА: Должно было выбросить IndexError!")
    except IndexError as e:
        print(f"   ✓ IndexError при удалении: {e}")
    
    # Попытка добавить некорректный тип
    print("\n4. Попытка добавить некорректный тип:")
    try:
        collection.add(123)
        print("   ОШИБКА: Должно было выбросить TypeError!")
    except TypeError as e:
        print(f"   ✓ TypeError: {e}")
    
    try:
        collection.add(None)
        print("   ОШИБКА: Должно было выбросить TypeError!")
    except TypeError as e:
        print(f"   ✓ TypeError: {e}")
    
    print("\n" + "=" * 60)


def main():
    """Основная функция, запускающая все сценарии."""
    print("*" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ КОЛЛЕКЦИИ APARTMENTCOLLECTION")
    print("Лабораторная работа №2 - Коллекция объектов")
    print("*" * 60)
    
    # Запуск всех сценариев
    scenario_1_basic_operations()
    scenario_2_search_and_filter()
    scenario_3_sorting_and_indexing()
    scenario_4_edge_cases()
    
    print("\n" + "*" * 60)
    print("ВСЕ СЦЕНАРИИ УСПЕШНО ВЫПОЛНЕНЫ!")
    print("*" * 60)


if __name__ == "__main__":
    main()