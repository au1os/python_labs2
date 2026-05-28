"""
Модуль содержит класс Apartment - базовую сущность предметной области "Аренда квартир".

Класс Apartment реализует:
1. Хранение данных о квартире (площадь, цена, адрес, срок аренды)
2. Логическое состояние (арендована/свободна)
3. Инварианты (положительные числа, непустой адрес)
4. Метод __eq__ для сравнения квартир
5. Бизнес-методы (расчёт платежа, проверка дороговизны)
6. Магические методы (__str__, __repr__, __eq__)
7. Атрибут класса (счётчик созданных квартир)

Этот класс является основой для всех последующих лабораторных работ (ЛР2-ЛР7).
"""

from validate import validate_positive_float, validate_positive_int, validate_nonempty_string


class Apartment:
    """
    Класс, представляющий квартиру для аренды.
    
    Атрибуты класса:
        _total_apartments (int): Счётчик всех созданных экземпляров квартир
    
    Атрибуты экземпляра:
        _area (float): Площадь квартиры в квадратных метрах
        _price (float): Полная стоимость аренды в рублях
        _address (str): Адрес квартиры
        _rent_duration (int): Срок аренды в месяцах
        _is_rented (bool): Флаг состояния аренды (True - арендована, False - свободна)
    
    Инварианты:
        - area > 0 (площадь всегда положительная)
        - price > 0 (цена всегда положительная)
        - address не может быть пустой строкой
        - rent_duration > 0 (срок аренды положительный)
        - При _is_rented == True запрещено изменять area, price, address, rent_duration
    
    Пример использования:
        >>> apt = Apartment(50.0, 100000, "ул. Примерная, 1", 12)
        >>> print(apt)
        Квартира: ул. Примерная, 1
          Площадь: 50.0 м²
          Цена (всего): 100,000.00 руб.
          ...
    """
    
    # Атрибут класса - счётчик всех созданных квартир
    # Используется для отслеживания общего количества экземпляров
    _total_apartments = 0
    
    def __init__(self, area: float, price: float, address: str, rent_duration: int):
        """
        Инициализация объекта Apartment.
        
        Конструктор создаёт новую квартиру с заданными параметрами,
        выполняет валидацию данных и увеличивает счётчик квартир.
        
        Args:
            area (float): Площадь квартиры в м² (должна быть > 0)
            price (float): Цена аренды в рублях (должна быть > 0)
            address (str): Адрес квартиры (не должен быть пустым)
            rent_duration (int): Срок аренды в месяцах (должен быть > 0)
        
        Raises:
            TypeError: Если тип данных не соответствует ожидаемому
            ValueError: Если значение не проходит валидацию (отрицательное, пустое и т.д.)
        """
        # Валидация через отдельные методы из модуля validate
        # Каждый метод проверяет тип и значение, выбрасывая исключение при ошибке
        self._area = validate_positive_float(area, "Площадь")
        self._price = validate_positive_float(price, "Цена")
        self._address = validate_nonempty_string(address, "Адрес")
        self._rent_duration = validate_positive_int(rent_duration, "Срок аренды")
        
        # Логическое состояние: арендована или нет
        # Изначально квартира свободна (не арендована)
        self._is_rented = False
        
        # Увеличиваем счётчик созданных квартир
        # Этот атрибут общий для всех экземпляров класса
        Apartment._total_apartments += 1
    
    # Геттеры (свойства только для чтения)
    # Используем @property для предоставления контролируемого доступа к атрибутам
    
    @property
    def area(self) -> float:
        """
        Возвращает площадь квартиры.
        
        Returns:
            float: Площадь квартиры в м²
        """
        return self._area
    
    @property
    def price(self) -> float:
        """
        Возвращает цену аренды квартиры.
        
        Returns:
            float: Цена аренды в рублях
        """
        return self._price
    
    @property
    def address(self) -> str:
        """
        Возвращает адрес квартиры.
        
        Returns:
            str: Адрес квартиры
        """
        return self._address
    
    @property
    def rent_duration(self) -> int:
        """
        Возвращает срок аренды.
        
        Returns:
            int: Срок аренды в месяцах
        """
        return self._rent_duration
    
    @property
    def is_rented(self) -> bool:
        """
        Возвращает состояние аренды квартиры.
        
        Returns:
            bool: True если квартира арендована, False если свободна
        """
        return self._is_rented
    
    # Сеттеры (свойства для записи)
    # Учитывают состояние объекта - нельзя изменять арендованную квартиру
    
    @area.setter
    def area(self, new_area: float):
        """
        Устанавливает новую площадь квартиры.
        
        Args:
            new_area (float): Новая площадь квартиры
            
        Raises:
            RuntimeError: Если квартира арендована (изменение запрещено)
            TypeError/ValueError: Если новое значение не проходит валидацию
        """
        # Проверка состояния: нельзя изменять арендованную квартиру
        if self._is_rented:
            raise RuntimeError("Нельзя изменить площадь арендованной квартиры")
        # Валидация и установка нового значения
        self._area = validate_positive_float(new_area, "Площадь")
    
    @price.setter
    def price(self, new_price: float):
        """
        Устанавливает новую цену аренды.
        
        Args:
            new_price (float): Новая цена аренды
            
        Raises:
            RuntimeError: Если квартира арендована
            TypeError/ValueError: Если новое значение не проходит валидацию
        """
        if self._is_rented:
            raise RuntimeError("Нельзя изменить цену арендованной квартиры")
        self._price = validate_positive_float(new_price, "Цена")
    
    @address.setter
    def address(self, new_address: str):
        """
        Устанавливает новый адрес квартиры.
        
        Args:
            new_address (str): Новый адрес
            
        Raises:
            RuntimeError: Если квартира арендована
            TypeError/ValueError: Если новое значение не проходит валидацию
        """
        if self._is_rented:
            raise RuntimeError("Нельзя изменить адрес арендованной квартиры")
        self._address = validate_nonempty_string(new_address, "Адрес")
    
    @rent_duration.setter
    def rent_duration(self, new_duration: int):
        """
        Устанавливает новый срок аренды.
        
        Args:
            new_duration (int): Новый срок в месяцах
            
        Raises:
            RuntimeError: Если квартира арендована
            TypeError/ValueError: Если новое значение не проходит валидацию
        """
        if self._is_rented:
            raise RuntimeError("Нельзя изменить срок аренды арендованной квартиры")
        self._rent_duration = validate_positive_int(new_duration, "Срок аренды")
    
    # Методы изменения состояния (изменяют флаг _is_rented)
    
    def rent(self) -> None:
        """
        Сдаёт квартиру в аренду (изменяет состояние на "арендована").
        
        Метод переводит квартиру в состояние "арендована", после чего
        запрещается изменение основных атрибутов (area, price, address, rent_duration).
        
        Raises:
            RuntimeError: Если квартира уже арендована
        """
        # Проверка: нельзя сдать уже арендованную квартиру
        if self._is_rented:
            raise RuntimeError("Квартира уже арендована")
        # Изменяем состояние
        self._is_rented = True
        print(f"Квартира по адресу {self._address} успешно арендована.")
    
    def vacate(self) -> None:
        """
        Освобождает квартиру (прекращает аренду).
        
        Метод переводит квартиру в состояние "свободна", разрешая
        последующее изменение атрибутов.
        
        Raises:
            RuntimeError: Если квартира не находится в аренде
        """
        # Проверка: нельзя освободить свободную квартиру
        if not self._is_rented:
            raise RuntimeError("Квартира не находится в аренде")
        # Изменяем состояние
        self._is_rented = False
        print(f"Квартира по адресу {self._address} освобождена.")
    
    # Бизнес-методы (выполняют предметные вычисления)
    
    def calculate_monthly_payment(self) -> float:
        """
        Рассчитывает ежемесячный платёж за квартиру.
        
        Returns:
            float: Сумма ежемесячного платежа в рублях
        """
        # Расчёт ежемесячного платежа: общая цена / срок аренды
        return self._price / self._rent_duration
    
    def is_expensive(self, threshold: float) -> bool:
        """
        Проверяет, является ли квартира дорогой (дороже заданного порога).
        
        Args:
            threshold (float): Порог стоимости в рублях
            
        Returns:
            bool: True если цена квартиры выше порога, иначе False
        """
        # Сравнение полной стоимости аренды с заданным порогом
        return self._price > threshold
    
    # Магические методы (перегрузка операторов)
    
    def __str__(self) -> str:
        """
        Возвращает человекочитаемое представление квартиры.
        
        Метод вызывается при использовании str(apartment) или print(apartment).
        Возвращает многострочную строку с полной информацией о квартире.
        
        Returns:
            str: Форматированное описание квартиры
        """
        # Определяем статус для вывода
        status = "Арендована" if self._is_rented else "Свободна"
        # Формируем многострочное представление
        return (f"Квартира: {self._address}\n"
                f"  Площадь: {self._area:.1f} м²\n"
                f"  Цена (всего): {self._price:,.2f} руб.\n"
                f"  Срок аренды: {self._rent_duration} мес.\n"
                f"  Ежемесячный платёж: {self.calculate_monthly_payment():,.2f} руб.\n"
                f"  Статус: {status}")
    
    def __repr__(self) -> str:
        """
        Возвращает техническое (каноническое) представление квартиры.
        
        Метод вызывается при использовании repr(apartment) или в интерактивной консоли.
        Возвращает строку, по которой (теоретически) можно воссоздать объект.
        
        Returns:
            str: Техническое представление объекта
        """
        return (f"Apartment(area={self._area}, price={self._price}, "
                f"address='{self._address}', rent_duration={self._rent_duration})")
    
    def __eq__(self, other) -> bool:
        """
        Сравнивает две квартиры на равенство.
        
        Квартиры считаются равными, если совпадают их адрес и площадь.
        Метод вызывается при использовании оператора ==.
        
        Args:
            other: Другой объект для сравнения
            
        Returns:
            bool: True если квартиры равны (одинаковый адрес и площадь), иначе False
        """
        # Сравниваем квартиры по адресу и площади
        # Сначала проверяем тип - сравнивать можно только с Apartment
        if not isinstance(other, Apartment):
            return False
        # Сравниваем по двум критериям: адрес И площадь
        return self._address == other._address and self._area == other._area
    
    # Метод для работы с атрибутом класса
    
    @classmethod
    def get_total_apartments(cls) -> int:
        """
        Возвращает общее количество созданных квартир.
        
        Метод класса (декоратор @classmethod), поэтому обращается к атрибуту класса,
        а не экземпляра. Может вызываться как через класс, так и через экземпляр.
        
        Returns:
            int: Общее количество экземпляров Apartment, созданных с начала работы программы
        """
        return cls._total_apartments