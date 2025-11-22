<<<<<<< HEAD
import argparse
import sys
import os
import urllib.request
import urllib.error
import json
from typing import List, Optional

class DependencyConfig:
=======
"""
Этап 1
"""

import argparse
import sys
import os
from typing import List, Optional

class DependencyConfig:
    """Класс для хранения конфигурации приложения"""
>>>>>>> 6e39842f0b1151d8592cb4c443d95825c74bb3a0
    def __init__(self):
        self.package_name = None
        self.repo_url = None
        self.test_mode = False
        self.ascii_tree = False
        self.max_depth = None
        self.output_file = None

<<<<<<< HEAD
class DependencyData:
    def __init__(self):
        self.direct_dependencies = []

class DependencyVisualizerStage2:
    
    def __init__(self, config):
        self.config = config
        self.data = DependencyData()
    
    def fetch_nuget_dependencies(self, package_name):
        """Получение зависимостей пакета из NuGet API"""
        try:
            print(f"Поиск информации о пакете '{package_name}'...")
            
            versions_url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/index.json"
            
            with urllib.request.urlopen(versions_url, timeout=10) as response:
                versions_data = json.loads(response.read().decode('utf-8'))
            
            versions = versions_data.get('versions', [])
            
            if not versions:
                print(f"Пакет {package_name} не найден или нет версий")
                return []
                
            target_version = versions[-1]
            print(f"Найдена версия: {target_version}")
            
            nuspec_url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/{target_version}/{package_name.lower()}.nuspec"
            
            with urllib.request.urlopen(nuspec_url, timeout=10) as nuspec_response:
                nuspec_content = nuspec_response.read().decode('utf-8')
                dependencies = self.parse_nuspec_dependencies(nuspec_content)
                print(f"Найдено зависимостей: {len(dependencies)}")
                return dependencies
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"Пакет {package_name} не найден в NuGet")
            else:
                print(f"HTTP ошибка при получении {package_name}: {e.code}")
            return []
        except Exception as e:
            print(f"Ошибка при получении зависимостей {package_name}: {e}")
            return []
    
    def parse_nuspec_dependencies(self, nuspec_content):
        """Парсинг зависимостей из .nuspec файла"""
        dependencies = []
        
        lines = nuspec_content.split('\n')
        in_dependencies = False
        
        for line in lines:
            line = line.strip()
            if '<dependencies>' in line:
                in_dependencies = True
            elif '</dependencies>' in line:
                in_dependencies = False
            elif in_dependencies and 'id="' in line:
                start = line.find('id="') + 4
                end = line.find('"', start)
                if start > 3 and end > start:
                    package_id = line[start:end]
                    if package_id not in dependencies:
                        dependencies.append(package_id)
        
        return dependencies
    
    def get_test_dependencies(self, test_file):
        """Получение зависимостей из тестового файла"""
        try:
            if os.path.exists(test_file):
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                dependencies = []
                for line in content.strip().split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(':')
                        if len(parts) >= 2:
                            dependencies.append(parts[0].strip())
                        else:
                            dependencies.append(line)
                
                return dependencies
            else:
                print(f"Тестовый файл {test_file} не найден")
                self.create_sample_test_file(test_file)
                return []
                
        except Exception as e:
            print(f"Ошибка при чтении тестового файла: {e}")
            return []
    
    def create_sample_test_file(self, filename):
        """Создание примера тестового файла"""
        sample_content = """# Пример тестового файла зависимостей
# Формат: ИмяПакета:Версия

System.Text.Json:7.0.0
Microsoft.Extensions.DependencyInjection:7.0.0
Microsoft.Extensions.Logging:7.0.0
Newtonsoft.Json:13.0.1
AutoMapper:12.0.0
"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(sample_content)
            print(f"Создан пример тестового файла: {filename}")
        except Exception as e:
            print(f"Не удалось создать тестовый файл: {e}")
    
    def print_direct_dependencies(self):
        """Вывод прямых зависимостей на экран - требование этапа"""
        print("\nПрямые зависимости пакета '{}':".format(self.config.package_name))
        
        if not self.data.direct_dependencies:
            print("  (нет зависимостей)")
        else:
            for i, dep in enumerate(self.data.direct_dependencies, 1):
                print(f"  {i}. {dep}")
    
    def run_stage2(self):
        """Основной метод выполнения второго этапа"""
        print("\n" + "=" * 50)
        print("Запуск этапа 2: Сбор данных о зависимостях")
        print("=" * 50)
        
        try:
            if self.config.test_mode:
                print(f"Режим тестирования: получение зависимостей из файла {self.config.repo_url}")
                self.data.direct_dependencies = self.get_test_dependencies(self.config.repo_url)
            else:
                print(f"Получение зависимостей из NuGet репозитория")
                self.data.direct_dependencies = self.fetch_nuget_dependencies(self.config.package_name)
            
            # Вывод прямых зависимостей - требование этапа
            self.print_direct_dependencies()
            
            print("Выполненные требования:")
            print("  - Использован формат пакетов .NET (NuGet)")
            print("  - Извлечена информация о прямых зависимостях")
            print("  - Вывод на экран всех прямых зависимостей")
            
            return self.data
            
        except Exception as e:
            print(f"Ошибка при выполнении этапа 2: {e}")
            return None

def main():
    # Для тестирования второго этапа отдельно
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=str, required=True)
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--test-mode", action="store_true")
    
    args = parser.parse_args()
    
    config = DependencyConfig()
    config.package_name = args.package
    config.repo_url = args.repo
    config.test_mode = args.test_mode
    
    visualizer = DependencyVisualizerStage2(config)
    data = visualizer.run_stage2()
    
    if data:
        print("\nДанные готовы для этапа 3")
        print(f"Найдено зависимостей: {len(data.direct_dependencies)}")
    else:
        print("\nЭтап 2 не завершен")
=======
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
>>>>>>> 6e39842f0b1151d8592cb4c443d95825c74bb3a0

if __name__ == "__main__":
    main()