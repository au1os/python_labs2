from validate import validate_positive_float, validate_positive_int, validate_nonempty_string

class Apartment:
    _total_apartments = 0

    def __init__(self, area: float, price: float, address: str, rent_duration: int):
        
        # Валидация через отдельные методы
        self._area = validate_positive_float(area, "Площадь")
        self._price = validate_positive_float(price, "Цена")
        self._address = validate_nonempty_string(address, "Адрес")
        self._rent_duration = validate_positive_int(rent_duration, "Срок аренды")
        
        # Логическое состояние: арендована или нет
        self._is_rented = False
        
        Apartment._total_apartments += 1

    # Геттеры
    @property
    def area(self) -> float:
        return self._area

    @property
    def price(self) -> float:
        return self._price

    @property
    def address(self) -> str:
        return self._address

    @property
    def rent_duration(self) -> int:
        return self._rent_duration

    @property
    def is_rented(self) -> bool: # Состояние аренды (арендовано или нет)
        return self._is_rented

    # Сеттеры, учитывающие состояние объекта
    @area.setter
    def area(self, new_area: float):
        if self._is_rented:
            raise RuntimeError("Нельзя изменить площадь арендованной квартиры")
        self._area = validate_positive_float(new_area, "Площадь")

    @price.setter
    def price(self, new_price: float):
        if self._is_rented:
            raise RuntimeError("Нельзя изменить цену арендованной квартиры")
        self._price = validate_positive_float(new_price, "Цена")

    @address.setter
    def address(self, new_address: str):
        if self._is_rented:
            raise RuntimeError("Нельзя изменить адрес арендованной квартиры")
        self._address = validate_nonempty_string(new_address, "Адрес")

    @rent_duration.setter
    def rent_duration(self, new_duration: int):
        if self._is_rented:
            raise RuntimeError("Нельзя изменить срок аренды арендованной квартиры")
        self._rent_duration = validate_positive_int(new_duration, "Срок аренды")

    # Свободные методы класса, изменяющие состояния
    def rent(self) -> None:
        if self._is_rented:
            raise RuntimeError("Квартира уже арендована")
        self._is_rented = True
        print(f"Квартира по адресу {self._address} успешно арендована.")

    def vacate(self) -> None:
        if not self._is_rented:
            raise RuntimeError("Квартира не находится в аренде")
        self._is_rented = False
        print(f"Квартира по адресу {self._address} освобождена.")

    # Бизнес-методы
    def calculate_monthly_payment(self) -> float:
        # Расчёт ежемесячного платежа
        return self._price / self._rent_duration

    def is_expensive(self, threshold: float) -> bool:
        # Проверка на бедного, сравнение стоимости аренды с капиталом арендатора
        return self._price > threshold

    # Магические методы
    def __str__(self) -> str:
        status = "Арендована" if self._is_rented else "Свободна"
        return (f"Квартира: {self._address}\n"
                f"  Площадь: {self._area:.1f} м²\n"
                f"  Цена (всего): {self._price:,.2f} руб.\n"
                f"  Срок аренды: {self._rent_duration} мес.\n"
                f"  Ежемесячный платёж: {self.calculate_monthly_payment():,.2f} руб.\n"
                f"  Статус: {status}")

    def __repr__(self) -> str:
        return (f"Apartment(area={self._area}, price={self._price}, "
                f"address='{self._address}', rent_duration={self._rent_duration})")

    def __eq__(self, other) -> bool:
        # Сравниваем квартиры по адресу и площади
        if not isinstance(other, Apartment):
            return False
        return self._address == other._address and self._area == other._area

    # ----- Метод для доступа к атрибуту класса (демонстрация) -----
    @classmethod
    def get_total_apartments(cls) -> int:
        """Возвращает общее количество созданных квартир."""
        return cls._total_apartments