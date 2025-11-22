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
    
    def get_dependencies_dfs(self, start_package: str, max_depth: int = None, current_depth: int = 0) -> Dict[str, List[str]]:
        if start_package in self.visited or (max_depth is not None and current_depth > max_depth):
            return {}
            
        self.visited.add(start_package)
        result = {start_package: self.graph.get(start_package, [])}
        
        for dep in self.graph.get(start_package, []):
            result.update(self.get_dependencies_dfs(dep, max_depth, current_depth + 1))
            
        return result

class DependencyVisualizerStage3:
    
    def __init__(self, config):
        self.config = config
        self.data = DependencyData()
        self.dependency_graph = DependencyGraph()
    
    def fetch_nuget_dependencies(self, package_name):
        try:
            versions_url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/index.json"
            
            with urllib.request.urlopen(versions_url, timeout=10) as response:
                versions_data = json.loads(response.read().decode('utf-8'))
            
            versions = versions_data.get('versions', [])
            
            if not versions:
                return []
                
            target_version = versions[-1]
            
            nuspec_url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/{target_version}/{package_name.lower()}.nuspec"
            
            with urllib.request.urlopen(nuspec_url, timeout=10) as nuspec_response:
                nuspec_content = nuspec_response.read().decode('utf-8')
                return self.parse_nuspec_dependencies(nuspec_content)
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"Пакет {package_name} не найден в NuGet")
            return []
        except Exception as e:
            print(f"Ошибка при получении зависимостей {package_name}: {e}")
            return []
    
    def parse_nuspec_dependencies(self, nuspec_content):
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
        try:
            if os.path.exists(test_file):
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                dependencies = []
                for line in content.strip().split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(':')
                        if len(parts) >= 1:
                            dependencies.append(parts[0].strip())
                
                return dependencies
            else:
                return []
                
        except Exception as e:
            print(f"Ошибка при чтении тестового файла: {e}")
            return []
    
    def build_dependency_graph_bfs(self):
        print("Построение графа зависимостей (BFS без рекурсии)...")
        
        queue = deque([(self.config.package_name, 0)])
        visited = set()
        cyclic_dependencies = set()
        
        while queue:
            current_package, depth = queue.popleft()
            
            if self.config.max_depth is not None and depth >= self.config.max_depth:
                print(f"Достигнута максимальная глубина {self.config.max_depth} для {current_package}")
                continue
                
            if current_package in visited:
                cyclic_dependencies.add(current_package)
                continue
                
            visited.add(current_package)
            print(f"Анализ {current_package} (уровень {depth})")
            
            if self.config.test_mode:
                dependencies = self.get_test_dependencies(self.config.repo_url)
            else:
                dependencies = self.fetch_nuget_dependencies(current_package)
            
            # Фильтрация пакетов по подстроке
            if self.config.filter_substring:
                dependencies = [dep for dep in dependencies if self.config.filter_substring not in dep]
            
            self.dependency_graph.add_dependency(current_package, dependencies)
            
            for dep in dependencies:
                if dep not in visited:
                    queue.append((dep, depth + 1))
        
        if cyclic_dependencies:
            print(f"Обнаружены циклические зависимости: {', '.join(cyclic_dependencies)}")
    
    def build_dependency_graph_dfs(self):
        print("Построение графа зависимостей (DFS с рекурсией)...")
        self._build_dfs_recursive(self.config.package_name, 0, set(), set())
    
    def _build_dfs_recursive(self, package, depth, visited, cyclic_deps):
        if self.config.max_depth is not None and depth >= self.config.max_depth:
            print(f"Достигнута максимальная глубина {self.config.max_depth} для {package}")
            return
            
        if package in visited:
            cyclic_deps.add(package)
            return
            
        visited.add(package)
        print(f"Анализ {package} (уровень {depth})")
        
        if self.config.test_mode:
            dependencies = self.get_test_dependencies(self.config.repo_url)
        else:
            dependencies = self.fetch_nuget_dependencies(package)
        
        # Фильтрация пакетов по подстроке
        if self.config.filter_substring:
            dependencies = [dep for dep in dependencies if self.config.filter_substring not in dep]
        
        self.dependency_graph.add_dependency(package, dependencies)
        
        for dep in dependencies:
            self._build_dfs_recursive(dep, depth + 1, visited, cyclic_deps)
        
        if cyclic_deps:
            print(f"Обнаружены циклические зависимости: {', '.join(cyclic_deps)}")
    
    def parse_test_repository_file(self, file_path):
        """Парсинг тестового файла репозитория с пакетами в виде больших букв"""
        graph = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        package, deps_str = line.split(':', 1)
                        package = package.strip()
                        dependencies = [dep.strip() for dep in deps_str.split(',') if dep.strip()]
                        graph[package] = dependencies
            return graph
        except Exception as e:
            print(f"Ошибка при чтении тестового файла: {e}")
            return {}
    
    def demonstrate_test_repository(self):
        """Демонстрация работы с тестовым репозиторием"""
        if not self.config.test_mode:
            return
        
        print("\nДемонстрация работы с тестовым репозиторием:")
        test_graph = self.parse_test_repository_file(self.config.repo_url)
        
        if not test_graph:
            print("Не удалось загрузить тестовый граф")
            return
        
        # Анализ нескольких пакетов из тестового графа
        test_packages = list(test_graph.keys())[:3]
        
        for package in test_packages:
            print(f"\nАнализ пакета {package}:")
            dependencies = test_graph.get(package, [])
            print(f"  Зависимости: {', '.join(dependencies)}")
            
            # Построение полного графа для тестового пакета
            self.dependency_graph = DependencyGraph()
            for pkg, deps in test_graph.items():
                self.dependency_graph.add_dependency(pkg, deps)
            
            full_deps = self.dependency_graph.get_dependencies_bfs(package, self.config.max_depth)
            print(f"  Полный граф ({len(full_deps)} пакетов): {list(full_deps.keys())}")
    
    def print_graph_statistics(self):
        """Вывод статистики графа"""
        all_dependencies = self.dependency_graph.get_dependencies_bfs(
            self.config.package_name, 
            self.config.max_depth
        )
        
        print(f"\nСтатистика графа зависимостей:")
        print(f"  Всего пакетов в графе: {len(all_dependencies)}")
        
        total_deps = sum(len(deps) for deps in all_dependencies.values())
        print(f"  Всего зависимостей: {total_deps}")
        
        packages_with_deps = [pkg for pkg, deps in all_dependencies.items() if deps]
        print(f"  Пакеты с зависимостями: {len(packages_with_deps)}")
        
        if packages_with_deps:
            print(f"  Примеры: {', '.join(packages_with_deps[:3])}")
    
    def run_stage3(self):
        print("\n" + "=" * 50)
        print("Запуск этапа 3: Основные операции с графом зависимостей")
        print("=" * 50)
        
        try:
            # Построение графа зависимостей BFS без рекурсии
            self.build_dependency_graph_bfs()
            
            # Демонстрация работы с тестовым репозиторием
            if self.config.test_mode:
                self.demonstrate_test_repository()
            
            # Вывод статистики
            self.print_graph_statistics()
            
            print("\nЭтап 3 выполнен успешно")
            print("Выполненные требования:")
            print("  - Построение графа алгоритмом BFS без рекурсии")
            print("  - Учет максимальной глубины анализа")
            print("  - Обработка циклических зависимостей")
            print("  - Поддержка тестового режима")
            print("  - Фильтрация пакетов по подстроке")
            
            return self.dependency_graph
            
        except Exception as e:
            print(f"Ошибка при выполнении этапа 3: {e}")
            return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=str, required=True)
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--filter-substring", type=str, help="Подстрока для фильтрации пакетов")
    
    args = parser.parse_args()
    
    config = DependencyConfig()
    config.package_name = args.package
    config.repo_url = args.repo
    config.test_mode = args.test_mode
    config.max_depth = args.max_depth
    config.filter_substring = args.filter_substring
    
    visualizer = DependencyVisualizerStage3(config)
    graph = visualizer.run_stage3()
    
    if graph:
        print("\nГраф готов для этапа 4")
    else:
        print("\nЭтап 3 не завершен")

if __name__ == "__main__":
    main()