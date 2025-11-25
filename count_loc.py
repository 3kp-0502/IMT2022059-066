import os
import re

def count_sloc(directory):
    total_lines = 0
    total_sloc = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    
                    for line in lines:
                        stripped = line.strip()
                        # Skip empty lines and comments
                        if stripped and not stripped.startswith('#'):
                            total_sloc += 1
                            
    return total_lines, total_sloc

if __name__ == "__main__":
    src_dir = "src"
    total, sloc = count_sloc(src_dir)
    print(f"Total Lines: {total}")
    print(f"Source Lines of Code (SLOC) - excluding comments/blanks: {sloc}")
