"""
Модуль содержит CLI-интерфейс приложения - меню, ввод/вывод данных.
Весь пользовательский интерфейс реализован здесь.
"""

from typing import List, Optional
from pathlib import Path
import sys

# Добавляем путь к lab01 для импорта базового класса
lab01_path = Path(__file__).parent.parent / "lab01"
sys.path.insert(0, str(lab01_path))

from model import Apartment
from exceptions import (
    ApartmentError,
    ApartmentNotFoundError,
    DuplicateApartmentError,
    InvalidApartmentError,
    ApartmentOperationError,
    StorageError,
    ConfirmationError
)
from app import ApartmentApp


class ApartmentCLI:
    """
    Класс CLI-интерфейса приложения.
    Отвечает за взаимодействие с пользователем.
    
    Attributes:
        app (ApartmentApp): Экземпляр приложения с бизнес-логикой
    """
    
    def __init__(self, app: ApartmentApp):
        """
        Инициализация CLI.
        
        Args:
            app: Экземпляр приложения
        """
        self.app = app
    
    def clear_screen(self) -> None:
        """Очищает экран консоли."""
        # Для Windows
        if sys.platform == "win32":
            import os
            os.system("cls")
        # Для Linux/Mac
        else:
            import os
            os.system("clear")
    
    def print_header(self, title: str) -> None:
        """
        Выводит заголовок раздела.
        
        Args:
            title: Текст заголовка
        """
        width = 60
        print("\n" + "=" * width)
        print(f" {title} ".center(width, "="))
        print("=" * width)
    
    def print_separator(self, char: str = "-", width: int = 60) -> None:
        """
        Выводит разделительную линию.
        
        Args:
            char: Символ разделителя
            width: Ширина линии
        """
        print(char * width)
    
    def print_apartment(self, apartment: Apartment, index: Optional[int] = None) -> None:
        """
        Форматированный вывод информации о квартире.
        
        Args:
            apartment: Объект квартиры
            index: Опциональный индекс для вывода
        """
        prefix = f"{index}. " if index is not None else ""
        status = "🏠 Арендована" if apartment.is_rented else "✅ Свободна"
        
        print(f"{prefix}{apartment.address}")
        print(f"   Площадь: {apartment.area:.1f} м²")
        print(f"   Цена: {apartment.price:,.2f} руб.")
        print(f"   Срок аренды: {apartment.rent_duration} мес.")
        print(f"   Ежемесячный платёж: {apartment.calculate_monthly_payment():,.2f} руб.")
        print(f"   Статус: {status}")
    
    def print_apartments_list(self, apartments: List[Apartment], title: str = "Список квартир") -> None:
        """
        Форматированный вывод списка квартир.
        
        Args:
            apartments: Список квартир
            title: Заголовок списка
        """
        self.print_header(title)
        
        if not apartments:
            print("   Список пуст")
        else:
            print(f"   Найдено: {len(apartments)} квартир\n")
            for i, apt in enumerate(apartments, 1):
                self.print_apartment(apt, i)
                print()
    
    def print_menu(self) -> None:
        """Выводит главное меню приложения."""
        self.print_header("СИСТЕМА УПРАВЛЕНИЯ АРЕНДОЙ КВАРТИР")
        print("\n  ГЛАВНОЕ МЕНЮ\n")
        print("  1. Показать все квартиры")
        print("  2. Добавить квартиру")
        print("  3. Найти квартиру")
        print("  4. Фильтровать квартиры")
        print("  5. Сортировать квартиры")
        print("  6. Сдать квартиру в аренду")
        print("  7. Освободить квартиру")
        print("  8. Изменить квартиру")
        print("  9. Удалить квартиру")
        print(" 10. Статистика")
        print(" 11. Сохранить данные")
        print(" 12. Загрузить данные")
        print("  0. Выход")
        print()
    
    def get_user_choice(self, prompt: str = "Выберите пункт меню: ") -> Optional[int]:
        """
        Запрашивает выбор пользователя.
        
        Args:
            prompt: Текст приглашения
            
        Returns:
            Optional[int]: Выбранный пункт меню или None при ошибке
        """
        try:
            choice = input(prompt).strip()
            return int(choice)
        except ValueError:
            print("  ❌ Ошибка: введите число!")
            return None
    
    def get_input(self, prompt: str, required: bool = True) -> str:
        """
        Запрашивает ввод строки от пользователя.
        
        Args:
            prompt: Текст приглашения
            required: Обязательно ли поле
            
        Returns:
            str: Введённая строка
        """
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            print("  ❌ Поле обязательно для заполнения!")
    
    def get_float_input(self, prompt: str, min_value: float = 0) -> float:
        """
        Запрашивает ввод числа с плавающей точкой.
        
        Args:
            prompt: Текст приглашения
            min_value: Минимальное допустимое значение
            
        Returns:
            float: Введённое число
        """
        while True:
            try:
                value = float(input(prompt).strip())
                if value <= min_value:
                    print(f"  ❌ Значение должно быть больше {min_value}!")
                    continue
                return value
            except ValueError:
                print("  ❌ Ошибка: введите число!")
    
    def get_int_input(self, prompt: str, min_value: int = 0) -> int:
        """
        Запрашивает ввод целого числа.
        
        Args:
            prompt: Текст приглашения
            min_value: Минимальное допустимое значение
            
        Returns:
            int: Введённое число
        """
        while True:
            try:
                value = int(input(prompt).strip())
                if value <= min_value:
                    print(f"  ❌ Значение должно быть больше {min_value}!")
                    continue
                return value
            except ValueError:
                print("  ❌ Ошибка: введите целое число!")
    
    def confirm(self, message: str) -> bool:
        """
        Запрашивает подтверждение операции.
        
        Args:
            message: Текст вопроса
            
        Returns:
            bool: True если подтверждено
        """
        while True:
            response = input(f"  {message} (y/n): ").strip().lower()
            if response in ("y", "yes", "да", "д"):
                return True
            elif response in ("n", "no", "нет", "н"):
                return False
            else:
                print("  ❌ Введите 'y' для подтверждения или 'n' для отмены")
    
    def show_all_apartments(self) -> None:
        """Показывает все квартиры в коллекции."""
        apartments = self.app.collection
        self.print_apartments_list(apartments, "ВСЕ КВАРТИРЫ")
    
    def add_apartment(self) -> None:
        """Добавляет новую квартиру через ввод данных."""
        self.print_header("ДОБАВИТЬ КВАРТИРУ")
        print("\nВведите данные квартиры:\n")
        
        try:
            area = self.get_float_input("  Площадь (м²): ")
            price = self.get_float_input("  Цена аренды (руб.): ")
            address = self.get_input("  Адрес: ")
            rent_duration = self.get_int_input("  Срок аренды (мес.): ")
            
            apartment = self.app.add_apartment(area, price, address, rent_duration)
            print(f"\n✅ Квартира успешно добавлена!")
            self.print_apartment(apartment)
            
        except (DuplicateApartmentError, InvalidApartmentError, ApartmentError) as e:
            print(f"\n❌ Ошибка: {e}")
    
    def find_apartment(self) -> None:
        """Ищет квартиру по адресу."""
        self.print_header("ПОИСК КВАРТИРЫ")
        
        address = self.get_input("  Введите адрес для поиска: ")
        apartment = self.app.find_by_address(address)
        
        if apartment:
            print(f"\n✅ Найдена квартира:")
            self.print_apartment(apartment)
        else:
            print(f"\n❌ Квартира по адресу '{address}' не найдена")
    
    def filter_apartments(self) -> None:
        """Фильтрует квартиры по различным критериям."""
        self.print_header("ФИЛЬТР КВАРТИР")
        print("\nВыберите критерий фильтрации:\n")
        print("  1. По диапазону цен")
        print("  2. По диапазону площади")
        print("  3. По сроку аренды")
        print("  4. Свободные квартиры")
        print("  5. Арендованные квартиры")
        print("  6. Дорогие квартиры (выше порога)")
        print()
        
        choice = self.get_user_choice("  Ваш выбор: ")
        
        if choice == 1:
            min_price = self.get_float_input("  Минимальная цена: ")
            max_price = self.get_float_input("  Максимальная цена: ")
            apartments = self.app.filter_by_price_range(min_price, max_price)
            self.print_apartments_list(apartments, f"Квартиры по цене {min_price:,.0f} - {max_price:,.0f} руб.")
        
        elif choice == 2:
            min_area = self.get_float_input("  Минимальная площадь (м²): ")
            max_area = self.get_float_input("  Максимальная площадь (м²): ")
            apartments = self.app.filter_by_area_range(min_area, max_area)
            self.print_apartments_list(apartments, f"Квартиры по площади {min_area} - {max_area} м²")
        
        elif choice == 3:
            duration = self.get_int_input("  Срок аренды (мес.): ")
            apartments = self.app.filter_by_rent_duration(duration)
            self.print_apartments_list(apartments, f"Квартиры на срок {duration} мес.")
        
        elif choice == 4:
            apartments = self.app.get_available()
            self.print_apartments_list(apartments, "СВОБОДНЫЕ КВАРТИРЫ")
        
        elif choice == 5:
            apartments = self.app.get_rented()
            self.print_apartments_list(apartments, "АРЕНДОВАННЫЕ КВАРТИРЫ")
        
        elif choice == 6:
            threshold = self.get_float_input("  Порог цены (руб.): ")
            apartments = self.app.get_expensive(threshold)
            self.print_apartments_list(apartments, f"Квартиры дороже {threshold:,.0f} руб.")
        
        else:
            print("  ❌ Некорректный выбор")
    
    def sort_apartments(self) -> None:
        """Сортирует квартиры по выбранному критерию."""
        self.print_header("СОРТИРОВКА КВАРТИР")
        print("\nВыберите критерий сортировки:\n")
        print("  1. По цене (по возрастанию)")
        print("  2. По цене (по убыванию)")
        print("  3. По площади (по возрастанию)")
        print("  4. По площади (по убыванию)")
        print("  5. По сроку аренды (по возрастанию)")
        print("  6. По сроку аренды (по убыванию)")
        print()
        
        choice = self.get_user_choice("  Ваш выбор: ")
        
        if choice == 1:
            apartments = self.app.sort_by_price(reverse=False)
            self.print_apartments_list(apartments, "КВАРТИРЫ ПО ЦЕНЕ (возрастание)")
        
        elif choice == 2:
            apartments = self.app.sort_by_price(reverse=True)
            self.print_apartments_list(apartments, "КВАРТИРЫ ПО ЦЕНЕ (убывание)")
        
        elif choice == 3:
            apartments = self.app.sort_by_area(reverse=False)
            self.print_apartments_list(apartments, "КВАРТИРЫ ПО ПЛОЩАДИ (возрастание)")
        
        elif choice == 4:
            apartments = self.app.sort_by_area(reverse=True)
            self.print_apartments_list(apartments, "КВАРТИРЫ ПО ПЛОЩАДИ (убывание)")
        
        elif choice == 5:
            apartments = self.app.sort_by_rent_duration(reverse=False)
            self.print_apartments_list(apartments, "КВАРТИРЫ ПО СРОКУ АРЕНДЫ (возрастание)")
        
        elif choice == 6:
            apartments = self.app.sort_by_rent_duration(reverse=True)
            self.print_apartments_list(apartments, "КВАРТИРЫ ПО СРОКУ АРЕНДЫ (убывание)")
        
        else:
            print("  ❌ Некорректный выбор")
    
    def rent_apartment(self) -> None:
        """Сдаёт квартиру в аренду."""
        self.print_header("СДАТЬ КВАРТИРУ В АРЕНДУ")
        
        address = self.get_input("  Введите адрес квартиры: ")
        
        try:
            apartment = self.app.rent_apartment(address)
            print(f"\n✅ Квартира успешно сдана в аренду!")
            self.print_apartment(apartment)
        except (ApartmentNotFoundError, ApartmentOperationError) as e:
            print(f"\n❌ Ошибка: {e}")
    
    def vacate_apartment(self) -> None:
        """Освобождает квартиру."""
        self.print_header("ОСВОБОДИТЬ КВАРТИРУ")
        
        address = self.get_input("  Введите адрес квартиры: ")
        
        try:
            apartment = self.app.vacate_apartment(address)
            print(f"\n✅ Квартира успешно освобождена!")
            self.print_apartment(apartment)
        except (ApartmentNotFoundError, ApartmentOperationError) as e:
            print(f"\n❌ Ошибка: {e}")
    
    def update_apartment(self) -> None:
        """Изменяет данные квартиры."""
        self.print_header("ИЗМЕНИТЬ КВАРТИРУ")
        
        address = self.get_input("  Введите адрес квартиры: ")
        apartment = self.app.find_by_address(address)
        
        if not apartment:
            print(f"\n❌ Квартира по адресу '{address}' не найдена")
            return
        
        print(f"\nТекущие данные:")
        self.print_apartment(apartment)
        
        if apartment.is_rented:
            print("\n❌ Нельзя изменить арендованную квартиру!")
            return
        
        print("\nВведите новые данные (оставьте пустым, чтобы не менять):")
        
        try:
            area_input = input("  Площадь (м²): ").strip()
            price_input = input("  Цена (руб.): ").strip()
            address_input = input("  Адрес: ").strip()
            duration_input = input("  Срок аренды (мес.): ").strip()
            
            kwargs = {}
            if area_input:
                kwargs["area"] = float(area_input)
            if price_input:
                kwargs["price"] = float(price_input)
            if address_input:
                kwargs["address"] = address_input
            if duration_input:
                kwargs["rent_duration"] = int(duration_input)
            
            if kwargs:
                apartment = self.app.update_apartment(address, **kwargs)
                print(f"\n✅ Квартира успешно обновлена!")
                self.print_apartment(apartment)
            else:
                print("\n❌ Не введено ни одного поля для изменения")
                
        except (ValueError, ApartmentError) as e:
            print(f"\n❌ Ошибка: {e}")
    
    def delete_apartment(self) -> None:
        """Удаляет квартиру."""
        self.print_header("УДАЛИТЬ КВАРТИРУ")
        
        address = self.get_input("  Введите адрес квартиры: ")
        apartment = self.app.find_by_address(address)
        
        if not apartment:
            print(f"\n❌ Квартира по адресу '{address}' не найдена")
            return
        
        print(f"\nВы собираетесь удалить квартиру:")
        self.print_apartment(apartment)
        
        if not self.confirm("Вы уверены?"):
            print("\n❌ Удаление отменено")
            return
        
        try:
            self.app.remove_apartment(address)
            print(f"\n✅ Квартира успешно удалена!")
        except ApartmentNotFoundError as e:
            print(f"\n❌ Ошибка: {e}")
    
    def show_statistics(self) -> None:
        """Показывает статистику по коллекции."""
        self.print_header("СТАТИСТИКА")
        
        stats = self.app.get_statistics()
        
        print(f"\n  Всего квартир: {stats['total']}")
        print(f"  Свободных: {stats['available']}")
        print(f"  Арендованных: {stats['rented']}")
        print(f"  Средняя цена: {stats['avg_price']:,.2f} руб.")
        print(f"  Средняя площадь: {stats['avg_area']:.1f} м²")
        print(f"  Минимальная цена: {stats['min_price']:,.2f} руб.")
        print(f"  Максимальная цена: {stats['max_price']:,.2f} руб.")
    
    def save_data(self) -> None:
        """Сохраняет данные в file."""
        self.print_header("СОХРАНЕНИЕ ДАННЫХ")
        
        try:
            self.app.save_data()
            print(f"\n✅ Данные успешно сохранены!")
            print(f"   Файл: {self.app._storage_path}")
        except StorageError as e:
            print(f"\n❌ Ошибка сохранения: {e}")
    
    def load_data(self) -> None:
        """Загружает данные из file."""
        self.print_header("ЗАГРУЗКА ДАННЫХ")
        
        try:
            count = self.app.load_data()
            print(f"\n✅ Данные успешно загружены!")
            print(f"   Загружено квартир: {count}")
        except StorageError as e:
            print(f"\n❌ Ошибка загрузки: {e}")
    
    def run(self) -> None:
        """Запускает CLI приложение."""
        # Автоматическая загрузка данных при запуске
        try:
            count = self.app.load_data()
            if count > 0:
                print(f"✅ Загружено {count} квартир из файла")
        except StorageError:
            pass  # Файл может не существовать
        
        while True:
            self.print_menu()
            choice = self.get_user_choice()
            
            if choice == 1:
                self.show_all_apartments()
            
            elif choice == 2:
                self.add_apartment()
            
            elif choice == 3:
                self.find_apartment()
            
            elif choice == 4:
                self.filter_apartments()
            
            elif choice == 5:
                self.sort_apartments()
            
            elif choice == 6:
                self.rent_apartment()
            
            elif choice == 7:
                self.vacate_apartment()
            
            elif choice == 8:
                self.update_apartment()
            
            elif choice == 9:
                self.delete_apartment()
            
            elif choice == 10:
                self.show_statistics()
            
            elif choice == 11:
                self.save_data()
            
            elif choice == 12:
                self.load_data()
            
            elif choice == 0:
                # Сохранение данных при выходе
                if self.app.count > 0:
                    if self.confirm("Сохранить данные перед выходом?"):
                        try:
                            self.app.save_data()
                            print("✅ Данные сохранены")
                        except StorageError:
                            pass
                print("\n👋 До свидания!")
                break
            
            else:
                print("  ❌ Некорректный выбор. Попробуйте снова.")
            
            # Пауза перед возвратом в меню
            input("\nНажмите Enter для продолжения...")