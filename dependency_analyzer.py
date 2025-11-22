import argparse
import sys
import os
import urllib.request
import urllib.error
import json
from typing import List, Optional

class DependencyConfig:
    def __init__(self):
        self.package_name = None
        self.repo_url = None
        self.test_mode = False
        self.ascii_tree = False
        self.max_depth = None
        self.output_file = None

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

if __name__ == "__main__":
    main()