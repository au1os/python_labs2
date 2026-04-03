from model import Apartment

def main():
    print("*" * 60)
    print("Демо работы класса Apartment")
    print("*" * 60)

    # Создание объектов и вывод через print 
    print("\n1. Создание двух квартир:")
    apar1 = Apartment(45.5, 75000, "ул. Ленина, д.10, кв.5", 12)
    apar2 = Apartment(62.0, 120000, "пр. Мира, д.25, кв.18", 6)
    print(apar1)
    print()
    print(apar2)

    # Сравнение двух объектов (проверка __eq__)
    print("\n2. Сравнение квартир:")
    apar3 = Apartment(45.5, 80000, "ул. Ленина, д.10, кв.5", 10)  # такой же адрес и площадь
    print(f"apt1 == apt3? {apar1 == apar3}")  # True
    print(f"apt1 == apt2? {apar1 == apar2}")  # False

    # Некорректное создание с try except
    print("\n3. Некорректное создание квартиры (площадь <=0):")
    try:
        bad_apar = Apartment(-10, 50000, "ул. Пушкина, 1", 6)
    except (TypeError, ValueError) as e:
        print(f"  Ошибка: {e}")

    print("\n   Некорректное создание (пустой адрес):")
    try:
        bad_apar2 = Apartment(50, 60000, "   ", 3)
    except (TypeError, ValueError) as e:
        print(f"  Ошибка: {e}")

    # Проверка сеттеров и ограничений
    print("\n4. Изменение цены через сеттер:")
    print(f"  До изменения: цена = {apar1.price}")
    apar1.price = 82000
    print(f"  После изменения: цена = {apar1.price}")

    print("\n   Попытка установить отрицательную площадь (должна быть ошибка):")
    try:
        apar1.area = -5
    except (TypeError, ValueError) as e:
        print(f"  Ошибка: {e}")

    # Смотрим атрибут класса, у нас он это счетчик квартир 
    print("\n5. Атрибут класса _total_apartments:")
    print(f"  Через класс: Apartment.get_total_apartments() = {Apartment.get_total_apartments()}")
    print(f"  Через экземпляр: apar1.get_total_apartments() = {apar1.get_total_apartments()}")

    # Бизнес-методы
    print("\n6. Бизнес-методы:")
    print(f"  Ежемесячный платёж для apt1: {apar1.calculate_monthly_payment():.2f} руб.")
    print(f"  apt1 дороже 100000 руб? {apar1.is_expensive(100000)}")
    print(f"  apt2 дороже 100000 руб? {apar2.is_expensive(100000)}")

    # Демо логического состояния и изменения поведения
    print("\n7. Демонстрация состояния 'арендована' и ограничений:")
    print("  Арендуем apt1...")
    apar1.rent()          # меняем состояние
    print(f"  Статус apt1: {'Арендована' if apar1.is_rented else 'Свободна'}")

    print("\n  Попытка изменить цену арендованной квартиры (должна быть ошибка):")
    try:
        apar1.price = 90000
    except RuntimeError as e:
        print(f"  Ошибка: {e}")

    print("\n  Попытка изменить площадь арендованной квартиры:")
    try:
        apar1.area = 50.0
    except RuntimeError as e:
        print(f"  Ошибка: {e}")

    print("\n  Освобождаем apar1...")
    apar1.vacate()
    print(f"  Статус apt1: {'Арендована' if apar1.is_rented else 'Свободна'}")

    print("\n  Теперь цена снова изменяема:")
    apar1.price = 90000
    print(f"  Новая цена: {apar1.price}")

    # __repr__
    print("\n8. Техническое представление (__repr__):")
    print(repr(apar1))

    print("\n" + "*" * 60)
    print("Демонстрация завершена.")

if __name__ == "__main__":
    main()