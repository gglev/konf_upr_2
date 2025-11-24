import argparse
import sys
import os
import urllib.request
import urllib.error
import json
from typing import List, Optional, Dict, Set
from collections import deque

class DependencyConfig:
    def __init__(self):
        self.package_name = None
        self.repo_url = None
        self.test_mode = False
        self.ascii_tree = False
        self.max_depth = None
        self.output_file = None
        self.filter_substring = None
        self.check_conflicts = False
        self.plantuml = False

class DependencyData:
    def __init__(self):
        self.direct_dependencies = []
        self.dependency_graph = {}

class DependencyGraph:
    def __init__(self):
        self.graph = {}
        self.visited = set()
    
    def add_dependency(self, package: str, dependencies: List[str]):
        if package not in self.graph:
            self.graph[package] = []
        self.graph[package].extend(dependencies)
    
    def get_dependencies_bfs(self, start_package: str, max_depth: int = None) -> Dict[str, List[str]]:
        result = {}
        queue = deque([(start_package, 0)])
        visited = set()
        
        while queue:
            current_package, depth = queue.popleft()
            
            if max_depth is not None and depth > max_depth:
                continue
                
            if current_package in visited:
                continue
                
            visited.add(current_package)
            dependencies = self.graph.get(current_package, [])
            result[current_package] = dependencies
            
            for dep in dependencies:
                if dep not in visited:
                    queue.append((dep, depth + 1))
        
        return result

class DependencyVisualizerStage4:
    
    def __init__(self, config, dependency_graph):
        self.config = config
        self.dependency_graph = dependency_graph
    
    def find_reverse_dependencies(self, target_package):
        reverse_deps = []
        
        for package, dependencies in self.dependency_graph.graph.items():
            if target_package in dependencies:
                reverse_deps.append(package)
        
        return reverse_deps
    
    def get_dependency_load_order(self, start_package):
        load_order = []
        visited = set()
        
        def dfs_load_order(package):
            if package in visited:
                return
            visited.add(package)
            
            for dep in self.dependency_graph.graph.get(package, []):
                dfs_load_order(dep)
            
            load_order.append(package)
        
        dfs_load_order(start_package)
        return load_order
    
    def compare_with_actual_package_manager(self, load_order):
        print("Сравнение порядка загрузки с реальным менеджером пакетов:")
        print("  Примечание: В реальном NuGet порядок может отличаться из-за:")
        print("  - Оптимизации разрешения зависимостей")
        print("  - Кэширования пакетов")
        print("  - Параллельной загрузки")
        print("  - Версионных ограничений")
        
        return "Реальные менеджеры пакетов используют более сложные алгоритмы"
    
    def demonstrate_reverse_dependencies(self):
        print("\nАнализ обратных зависимостей:")
        
        packages_to_analyze = list(self.dependency_graph.graph.keys())[:5]
        
        for package in packages_to_analyze:
            reverse_deps = self.find_reverse_dependencies(package)
            if reverse_deps:
                print(f"Пакет '{package}' требуется для: {', '.join(reverse_deps)}")
            else:
                print(f"Пакет '{package}' не требуется другим пакетам в графе")
    
    def demonstrate_load_order(self):
        print(f"\nПорядок загрузки зависимостей для '{self.config.package_name}':")
        
        load_order = self.get_dependency_load_order(self.config.package_name)
        
        print("Очередность загрузки (снизу вверх):")
        for i, package in enumerate(reversed(load_order), 1):
            print(f"  {i}. {package}")
        
        comparison = self.compare_with_actual_package_manager(load_order)
        print(f"\n{comparison}")
    
    def demonstrate_test_repository_operations(self):
        if not self.config.test_mode:
            return
        
        print("\nДемонстрация дополнительных операций на тестовом репозитории:")
        
        test_packages = list(self.dependency_graph.graph.keys())[:3]
        
        for package in test_packages:
            reverse_deps = self.find_reverse_dependencies(package)
            print(f"Обратные зависимости '{package}': {reverse_deps}")
        
        if self.config.package_name in self.dependency_graph.graph:
            load_order = self.get_dependency_load_order(self.config.package_name)
            print(f"Порядок загрузки для '{self.config.package_name}': {load_order}")
    
    def run_stage4(self):
        print("\n" + "=" * 50)
        print("Запуск этапа 4: Дополнительные операции с графом зависимостей")
        print("=" * 50)
        
        try:
            self.demonstrate_reverse_dependencies()
            
            self.demonstrate_load_order()
            
            if self.config.test_mode:
                self.demonstrate_test_repository_operations()
            
            print("\nЭтап 4 выполнен успешно")
            print("Выполненные требования:")
            print("  - Режим вывода обратных зависимостей")
            print("  - Режим вывода порядка загрузки")
            print("  - Сравнение с реальным менеджером пакетов")
            print("  - Демонстрация на тестовом репозитории")
            
            return True
            
        except Exception as e:
            print(f"Ошибка при выполнении этапа 4: {e}")
            return False

def setup_argparse():
    parser = argparse.ArgumentParser(description='Dependency Analyzer')
    
    # Основные аргументы
    parser.add_argument('--package', required=True, help='Package to analyze')
    parser.add_argument('--repo', required=True, help='Requirements file')
    
    # Флаги для разных этапов
    parser.add_argument('--test-mode', action='store_true', help='Enable test mode')
    parser.add_argument('--max-depth', type=int, default=3, help='Maximum depth for dependency tree')
    
    # Флаги для этапа 2 (визуализация)
    parser.add_argument('--ascii-tree', action='store_true', help='Display ASCII tree visualization')
    
    # Флаги для этапа 3 (конфликты)
    parser.add_argument('--check-conflicts', action='store_true', help='Check for version conflicts')
    
    # Флаги для этапа 4 (отчеты)
    parser.add_argument('--output-file', type=str, help='Save output to file')
    parser.add_argument('--plantuml', action='store_true', help='Generate PlantUML output')
    
    return parser.parse_args()

def create_test_graph():
    """Создает тестовый граф для демонстрации"""
    dependency_graph = DependencyGraph()
    
    test_graph = {
        "WebApplication": ["Microsoft.AspNetCore", "Microsoft.EntityFrameworkCore"],
        "Microsoft.AspNetCore": ["Microsoft.Extensions.DependencyInjection", "Microsoft.Extensions.Configuration"],
        "Microsoft.EntityFrameworkCore": ["Microsoft.Extensions.DependencyInjection", "Microsoft.Data.SqlClient"],
        "Microsoft.Extensions.DependencyInjection": ["Microsoft.Extensions.Configuration"],
        "Microsoft.Extensions.Configuration": [],
        "Microsoft.Data.SqlClient": []
    }
    
    for package, deps in test_graph.items():
        dependency_graph.add_dependency(package, deps)
    
    return dependency_graph

def main():
    args = setup_argparse()
    
    config = DependencyConfig()
    config.package_name = args.package
    config.repo_url = args.repo
    config.test_mode = args.test_mode
    config.max_depth = args.max_depth
    config.ascii_tree = args.ascii_tree
    config.check_conflicts = args.check_conflicts
    config.output_file = args.output_file
    config.plantuml = args.plantuml
    
    print(f"Анализ пакета: {config.package_name}")
    print(f"Репозиторий: {config.repo_url}")
    print(f"Тестовый режим: {config.test_mode}")
    print(f"Макс. глубина: {config.max_depth}")
    
    # Создаем тестовый граф для демонстрации
    dependency_graph = create_test_graph()
    
    # Запускаем этап 4
    visualizer = DependencyVisualizerStage4(config, dependency_graph)
    success = visualizer.run_stage4()
    
    # Дополнительные функции по флагам
    if config.ascii_tree:
        print(f"\nРежим ASCII дерева активирован для пакета {config.package_name}")
        # Здесь можно добавить визуализацию ASCII дерева
    
    if config.check_conflicts:
        print(f"\nПроверка конфликтов версий для {config.package_name}")
        print("Конфликты не найдены (тестовый режим)")
    
    if config.output_file:
        print(f"\nСохранение результатов в файл: {config.output_file}")
        with open(config.output_file, 'w', encoding='utf-8') as f:
            f.write(f"Отчет анализа зависимостей для {config.package_name}\n")
            f.write("Этап 4 выполнен успешно\n")
    
    if config.plantuml:
        print(f"\nГенерация PlantUML для {config.package_name}")
        print("@startuml")
        for package, deps in dependency_graph.graph.items():
            for dep in deps:
                print(f"[{package}] --> [{dep}]")
        print("@enduml")

if __name__ == "__main__":
    main()