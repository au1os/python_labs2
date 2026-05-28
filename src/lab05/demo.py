"""
Демонстрация работы с функциями как аргументами, стратегиями и делегатами.
Сценарии использования:
1. Полная цепочка filter → sort → apply
2. Замена стратегии без изменения кода коллекции
3. Демонстрация callable-объекта как стратегии
"""

from collection import ApartmentCollection
from strategies import (
    # Стратегии сортировки
    by_price, by_price_desc, by_area, by_area_desc, 
    by_rent_duration, by_monthly_payment, by_address,
    # Функции-фильтры
    is_available, is_rented, is_expensive, is_large, is_small, is_in_budget, has_short_rent,
    # Фабрики функций
    make_price_filter, make_min_area_filter, make_price_range_filter, make_discount_strategy,
    # Стратегии (callable-объекты)
    DiscountStrategy, MonthlyPaymentStrategy, PricePerSqmStrategy, AddressFormatter
)


def scenario_1_filter_sort_apply_chain():
    """
    Сценарий 1: Полная цепочка filter → sort → apply с выводом на каждом шаге.
    """
    print("=" * 60)
    print("СЦЕНАРИЙ 1: Полная цепочка filter → sort → apply")
    print("=" * 60)
    
    # Создание коллекции
    print("\n1. Создание коллекции:")
    collection = ApartmentCollection()
    
    collection.add(Apartment(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(Apartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6))
    collection.add(Apartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12))
    collection.add(Apartment(60.0, 120000, "ул. Центральная, д.20, кв.50", 6))
    collection.add(Apartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6))
    collection.add(Apartment(80.0, 200000, "ул. Комфортная, д.15, кв.30", 12))
    
    print(f"   Всего квартир: {len(collection)}")
    
    # Шаг 1: Фильтрация - только доступные квартиры
    print("\n2. Фильтрация: только доступные (не арендованные):")
    available = collection.filter_by(is_available)
    print(f"   Найдено доступных: {len(available)}")
    for apt in available:
        print(f"   - {apt.address}: {apt.price:,.2f} руб.")
    
    # Шаг 2: Сортировка - по цене (возрастание)
    print("\n3. Сортировка доступных по цене (возрастание):")
    sorted_by_price = available.sort_by(by_price)
    print("   После сортировки:")
    for i, apt in enumerate(sorted_by_price, 1):
        print(f"   {i}. {apt.address}: {apt.price:,.2f} руб.")
    
    # Шаг 3: Применение функции - расчёт ежемесячного платежа
    print("\n4. Применение функции: расчёт ежемесячного платежа:")
    monthly_payments = sorted_by_price.apply(MonthlyPaymentStrategy())
    print("   Результаты:")
    for i, (apt, payment) in enumerate(zip(sorted_by_price, monthly_payments), 1):
        print(f"   {i}. {apt.address}: {payment:,.2f} руб./мес.")
    
    # Полная цепочка в одну строку
    print("\n5. Полная цепочка в одну строку:")
    result = (collection
              .filter_by(is_available)
              .sort_by(by_price)
              .apply(lambda x: f"{x.address}: {x.calculate_monthly_payment():,.2f} руб./мес."))
    print("   Результат цепочки:")
    for item in result:
        print(f"   - {item}")
    
    print("\n" + "=" * 60)


def scenario_2_strategy_replacement():
    """
    Сценарий 2: Замена стратегии без изменения кода коллекции.
    Показывает, что при передаче другой функции результат меняется.
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 2: Замена стратегии без изменения кода коллекции")
    print("=" * 60)
    
    # Создание коллекции
    print("\n1. Создание коллекции:")
    collection = ApartmentCollection()
    
    collection.add(Apartment(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(Apartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6))
    collection.add(Apartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12))
    collection.add(Apartment(60.0, 120000, "ул. Центральная, д.20, кв.50", 6))
    collection.add(Apartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6))
    
    print(f"   Всего квартир: {len(collection)}")
    
    # Сортировка по разным стратегиям
    print("\n2. Сортировка по разным стратегиям:")
    
    print("\n   a) Сортировка по цене (возрастание):")
    sorted_price = collection.sort_by(by_price)
    for i, apt in enumerate(sorted_price, 1):
        print(f"      {i}. {apt.address}: {apt.price:,.2f} руб.")
    
    print("\n   b) Сортировка по цене (убывание):")
    sorted_price_desc = collection.sort_by(by_price_desc)
    for i, apt in enumerate(sorted_price_desc, 1):
        print(f"      {i}. {apt.address}: {apt.price:,.2f} руб.")
    
    print("\n   c) Сортировка по площади (возрастание):")
    sorted_area = collection.sort_by(by_area)
    for i, apt in enumerate(sorted_area, 1):
        print(f"      {i}. {apt.address}: {apt.area} м²")
    
    print("\n   d) Сортировка по сроку аренды:")
    sorted_duration = collection.sort_by(by_rent_duration)
    for i, apt in enumerate(sorted_duration, 1):
        print(f"      {i}. {apt.address}: {apt.rent_duration} мес.")
    
    # Фильтрация разными стратегиями
    print("\n3. Фильтрация разными стратегиями:")
    
    print("\n   a) Фильтр: доступные квартиры:")
    available = collection.filter_by(is_available)
    print(f"      Найдено: {len(available)}")
    
    print("\n   b) Фильтр: дорогие квартиры (>100000):")
    expensive = collection.filter_by(lambda x: is_expensive(x, 100000))
    print(f"      Найдено: {len(expensive)}")
    for apt in expensive:
        print(f"         - {apt.address}: {apt.price:,.2f} руб.")
    
    print("\n   c) Фильтр: большие квартиры (>=60 м²):")
    large = collection.filter_by(is_large)
    print(f"      Найдено: {len(large)}")
    for apt in large:
        print(f"         - {apt.address}: {apt.area} м²")
    
    print("\n   d) Фильтр: квартиры с короткой арендой (<=6 мес):")
    short_rent = collection.filter_by(has_short_rent)
    print(f"      Найдено: {len(short_rent)}")
    for apt in short_rent:
        print(f"         - {apt.address}: {apt.rent_duration} мес.")
    
    # Использование фабрик функций
    print("\n4. Использование фабрик функций:")
    
    print("\n   a) Фильтр по цене до 100000 (через фабрику):")
    budget_filter = make_price_filter(100000)
    budget_apts = collection.filter_by(budget_filter)
    print(f"      Найдено: {len(budget_apts)}")
    for apt in budget_apts:
        print(f"         - {apt.address}: {apt.price:,.2f} руб.")
    
    print("\n   b) Фильтр по диапазону цен 70000-120000 (через фабрику):")
    range_filter = make_price_range_filter(70000, 120000)
    range_apts = collection.filter_by(range_filter)
    print(f"      Найдено: {len(range_apts)}")
    for apt in range_apts:
        print(f"         - {apt.address}: {apt.price:,.2f} руб.")
    
    print("\n" + "=" * 60)


def scenario_3_callable_strategies():
    """
    Сценарий 3: Демонстрация callable-объекта как стратегии.
    """
    print("\n" + "=" * 60)
    print("СЦЕНАРИЙ 3: Callable-объекты как стратегии")
    print("=" * 60)
    
    # Создание коллекции
    print("\n1. Создание коллекции:")
    collection = ApartmentCollection()
    
    collection.add(Apartment(50.0, 100000, "ул. Примерная, д.1, кв.10", 12))
    collection.add(Apartment(35.0, 70000, "ул. Студенческая, д.5, кв.20", 6))
    collection.add(Apartment(120.0, 300000, "пр. Элитный, д.1, пентхаус", 12))
    collection.add(Apartment(60.0, 120000, "ул. Центральная, д.20, кв.50", 6))
    collection.add(Apartment(40.0, 90000, "ул. Премиум, д.10, кв.5", 6))
    
    print(f"   Всего квартир: {len(collection)}")
    
    # Использование callable-стратегий
    print("\n2. Использование callable-стратегий:")
    
    print("\n   a) Стратегия скидки 10%:")
    discount_10 = DiscountStrategy(10)
    discounted_prices = collection.apply(discount_10)
    print(f"      Стратегия: {discount_10}")
    for i, (apt, price) in enumerate(zip(collection, discounted_prices), 1):
        print(f"      {i}. {apt.address}: {price:,.2f} руб. (было {apt.price:,.2f} руб.)")
    
    print("\n   b) Стратегия скидки 20%:")
    discount_20 = DiscountStrategy(20)
    discounted_prices_20 = collection.apply(discount_20)
    print(f"      Стратегия: {discount_20}")
    for i, (apt, price) in enumerate(zip(collection, discounted_prices_20), 1):
        print(f"      {i}. {apt.address}: {price:,.2f} руб. (было {apt.price:,.2f} руб.)")
    
    print("\n   c) Стратегия расчёта ежемесячного платежа:")
    payment_strategy = MonthlyPaymentStrategy()
    payments = collection.apply(payment_strategy)
    print(f"      Стратегия: {payment_strategy}")
    for i, (apt, payment) in enumerate(zip(collection, payments), 1):
        print(f"      {i}. {apt.address}: {payment:,.2f} руб./мес.")
    
    print("\n   d) Стратегия расчёта цены за м²:")
    price_per_sqm = PricePerSqmStrategy()
    prices_per_sqm = collection.apply(price_per_sqm)
    print(f"      Стратегия: {price_per_sqm}")
    for i, (apt, price_sqm) in enumerate(zip(collection, prices_per_sqm), 1):
        print(f"      {i}. {apt.address}: {price_sqm:,.2f} руб./м²")
    
    print("\n   e) Форматтер адресов (короткий):")
    short_formatter = AddressFormatter(short=True)
    short_addresses = collection.apply(short_formatter)
    print(f"      Стратегия: {short_formatter}")
    for addr in short_addresses:
        print(f"      - {addr}")
    
    # Комбинирование стратегий
    print("\n3. Комбинирование стратегий:")
    print("\n   Доступные квартиры со скидкой 15% и сортировкой по цене:")
    result = (collection
              .filter_by(is_available)
              .sort_by(by_price)
              .apply(DiscountStrategy(15)))
    print(f"   Найдено: {len(result)}")
    for i, price in enumerate(result, 1):
        print(f"   {i}. Цена со скидкой: {price:,.2f} руб.")
    
    print("\n" + "=" * 60)


def main():
    """Основная функция, запускающая все сценарии."""
    print("*" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ С ФУНКЦИЯМИ КАК АРГУМЕНТАМИ")
    print("Лабораторная работа №5 - Функции как аргументы. Стратегии и делегаты.")
    print("*" * 60)
    
    # Запуск всех сценариев
    scenario_1_filter_sort_apply_chain()
    scenario_2_strategy_replacement()
    scenario_3_callable_strategies()
    
    print("\n" + "*" * 60)
    print("ВСЕ СЦЕНАРИИ УСПЕШНО ВЫПОЛНЕНЫ!")
    print("*" * 60)


if __name__ == "__main__":
    main()