import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='"'"'NuGet Package Dependency Visualizer'"'"')
    parser.add_argument('"'"'--package'"'"', '"'"'-p'"'"', required=True, help='"'"'Package name to analyze'"'"')
    parser.add_argument('"'"'--repository'"'"', '"'"'-r'"'"', help='"'"'Repository URL or test file path'"'"')
    parser.add_argument('"'"'--test-mode'"'"', '"'"'-t'"'"', action='"'"'store_true'"'"', help='"'"'Enable test mode'"'"')
    parser.add_argument('"'"'--ascii-tree'"'"', '"'"'-a'"'"', action='"'"'store_true'"'"', help='"'"'Display dependencies as ASCII tree'"'"')
    
    if len(sys.argv) == 1:
        print("Error: No arguments provided")
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    print("Configuration parameters (key-value format):")
    print(f"  package: {args.package}")
    print(f"  repository: {args.repository}")
    print(f"  test_mode: {args.test_mode}")
    print(f"  ascii_tree: {args.ascii_tree}")
    
    if args.test_mode and not args.repository:
        print("Error: Test mode requires repository file path")
        sys.exit(1)
    
    print(f"\nApplication configured successfully for package: {args.package}")

if __name__ == "__main__":
    main()
