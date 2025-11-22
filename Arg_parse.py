"""
Этап 1
"""

import argparse
import sys
import os
from typing import List, Optional

class DependencyConfig:
    """Класс для хранения конфигурации приложения"""
    def __init__(self):
        self.package_name = None
        self.repo_url = None
        self.test_mode = False
        self.ascii_tree = False
        self.max_depth = None
        self.output_file = None

class DependencyVisualizerStage1:
    """Реализация первого этапа - конфигурация CLI"""
    
    def __init__(self):
        self.config = DependencyConfig()
    
    def parse_arguments(self) -> argparse.Namespace:
        """Парсинг аргументов командной строки"""
        parser = argparse.ArgumentParser(
            description="Инструмент визуализации графа зависимостей для менеджера пакетов .NET (NuGet)",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Основные параметры
        parser.add_argument(
            "--package", 
            type=str, 
            required=True,
            help="Имя анализируемого пакета"
        )
        
        parser.add_argument(
            "--repo", 
            type=str, 
            required=True,
            help="URL-адрес репозитория или путь к файлу тестового репозитория"
        )
        
        # Дополнительные параметры
        parser.add_argument(
            "--test-mode", 
            action="store_true",
            help="Режим работы с тестовым репозиторием"
        )
        
        parser.add_argument(
            "--ascii-tree", 
            action="store_true",
            help="Режим вывода зависимостей в формате ASCII-дерева"
        )
        
        parser.add_argument(
            "--max-depth", 
            type=int,
            help="Максимальная глубина анализа зависимостей"
        )
        
        parser.add_argument(
            "--output-file", 
            type=str,
            help="Имя файла для сохранения результатов"
        )
        
        return parser.parse_args()
    
    def validate_arguments(self, args: argparse.Namespace) -> List[str]:
        """Валидация аргументов командной строки"""
        errors = []
        
        # Проверка обязательных параметров
        if not args.package or args.package.strip() == "":
            errors.append("Имя пакета не может быть пустым")
        
        if not args.repo or args.repo.strip() == "":
            errors.append("Репозиторий не может быть пустым")
        
        # Проверка числовых параметров
        if args.max_depth is not None and args.max_depth < 1:
            errors.append("Максимальная глубина должна быть положительным числом")
        
        # Проверка тестового режима
        if args.test_mode:
            if not os.path.exists(args.repo):
                errors.append(f"Тестовый файл не найден: {args.repo}")
            elif not os.path.isfile(args.repo):
                errors.append(f"Указанный путь не является файлом: {args.repo}")
        
        return errors
    
    def print_configuration(self, args: argparse.Namespace):
        """Вывод конфигурации в формате ключ-значение"""
        print("=" * 50)
        print("Конфигурация приложения")
        print("=" * 50)
        
        config_items = [
            ("Имя анализируемого пакета", args.package),
            ("URL репозитория/файл", args.repo),
            ("Режим тестового репозитория", "ВКЛ" if args.test_mode else "ВЫКЛ"),
            ("Режим ASCII-дерева", "ВКЛ" if args.ascii_tree else "ВЫКЛ"),
            ("Максимальная глубина", args.max_depth if args.max_depth else "неограничено"),
            ("Файл для сохранения", args.output_file if args.output_file else "не указан")
        ]
        
        for key, value in config_items:
            print(f"{key}: {value}")
        
        print("=" * 50)
    
    def run_stage1(self) -> Optional[DependencyConfig]:
        """Основной метод выполнения первого этапа"""
        print("Запуск 1 этапа: Минимальный прототип с конфигурацией")
        print("-" * 50)
        
        try:
            # Парсинг аргументов
            args = self.parse_arguments()
            
            # Валидация аргументов
            errors = self.validate_arguments(args)
            if errors:
                print("Ошибки в конфигурации:")
                for error in errors:
                    print(f"  - {error}")
                return None
            
            # Вывод конфигурации
            self.print_configuration(args)
            
            # Сохранение конфигурации
            self.config.package_name = args.package
            self.config.repo_url = args.repo
            self.config.test_mode = args.test_mode
            self.config.ascii_tree = args.ascii_tree
            self.config.max_depth = args.max_depth
            self.config.output_file = args.output_file
            
            # Успешное завершение этапа
            print("Этап 1 выполнен успешно")
            print("Выполненные требования:")
            print("  - Источник параметров - опции командной строки")
            print("  - Настраиваемые параметры: имя пакета, репозиторий, режимы")
            print("  - Вывод параметров в формате ключ-значение")
            print("  - Обработка ошибок для всех параметров")
            
            return self.config
            
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            return None

def main():
    """Точка входа для первого этапа"""
    visualizer = DependencyVisualizerStage1()
    config = visualizer.run_stage1()
    
    if config:
        print(f"  Пакет: {config.package_name}")
        print(f"  Репозиторий: {config.repo_url}")
        print(f"  Тестовый режим: {config.test_mode}")
    else:
        print("\nЭтап 1 не завершен из-за ошибок")

if __name__ == "__main__":
    main()