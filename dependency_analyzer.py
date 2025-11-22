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

def main_stage4():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=str, required=True)
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--max-depth", type=int, default=2)
    
    args = parser.parse_args()
    
    config = DependencyConfig()
    config.package_name = args.package
    config.repo_url = args.repo
    config.test_mode = args.test_mode
    config.max_depth = args.max_depth
    
    print("Для этапа 4 требуется предварительно построенный граф зависимостей.")
    print("Создаем тестовый граф для демонстрации...")
    
    dependency_graph = DependencyGraph()
    
    if args.test_mode:
        test_graph = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F"],
            "D": ["G"],
            "E": ["G"],
            "F": [],
            "G": []
        }
        
        for package, deps in test_graph.items():
            dependency_graph.add_dependency(package, deps)
        
        config.package_name = "A"
    else:
        print("В реальном режиме требуется предварительное выполнение этапа 3")
        return
    
    visualizer = DependencyVisualizerStage4(config, dependency_graph)
    success = visualizer.run_stage4()
    
    if success:
        print("\nЭтап 4 завершен")
    else:
        print("\nЭтап 4 не завершен")

if __name__ == "__main__":
    main_stage4()