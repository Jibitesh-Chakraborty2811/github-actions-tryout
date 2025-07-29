#!/usr/bin/env python3
"""
File Analyzer Script for GitHub Actions
Analyzes files in repository for print statements across multiple languages
"""

import os
import re
from pathlib import Path

def count_print_statements(file_path, content):
    """Count print statements in different file types"""
    file_ext = Path(file_path).suffix.lower()
    
    # Define patterns for different languages
    patterns = {
        '.py': [
            r'\bprint\s*\(',  # Python: print(...)
        ],
        '.js': [
            r'\bconsole\.log\s*\(',  # JavaScript: console.log(...)
            r'\bconsole\.info\s*\(',  # JavaScript: console.info(...)
            r'\bconsole\.warn\s*\(',  # JavaScript: console.warn(...)
            r'\bconsole\.error\s*\(',  # JavaScript: console.error(...)
        ],
        '.ts': [
            r'\bconsole\.log\s*\(',  # TypeScript: console.log(...)
            r'\bconsole\.info\s*\(',  # TypeScript: console.info(...)
            r'\bconsole\.warn\s*\(',  # TypeScript: console.warn(...)
            r'\bconsole\.error\s*\(',  # TypeScript: console.error(...)
        ],
        '.jsx': [
            r'\bconsole\.log\s*\(',  # React JSX: console.log(...)
        ],
        '.tsx': [
            r'\bconsole\.log\s*\(',  # React TSX: console.log(...)
        ],
        '.java': [
            r'\bSystem\.out\.print\w*\s*\(',  # Java: System.out.print*(...) 
        ],
        '.cpp': [
            r'\bstd::cout\s*<<',  # C++: std::cout <<
            r'\bcout\s*<<',      # C++: cout <<
            r'\bprintf\s*\(',    # C/C++: printf(...)
        ],
        '.c': [
            r'\bprintf\s*\(',    # C: printf(...)
        ],
        '.go': [
            r'\bfmt\.Print\w*\s*\(',  # Go: fmt.Print*(...) 
        ],
        '.rs': [
            r'\bprintln!\s*\(',  # Rust: println!(...)
            r'\bprint!\s*\(',    # Rust: print!(...)
        ],
        '.php': [
            r'\becho\s+',        # PHP: echo
            r'\bprint\s+',       # PHP: print
            r'\bprint_r\s*\(',   # PHP: print_r(...)
            r'\bvar_dump\s*\(',  # PHP: var_dump(...)
        ],
        '.rb': [
            r'\bputs\s+',        # Ruby: puts
            r'\bprint\s+',       # Ruby: print
            r'\bp\s+',           # Ruby: p
        ],
        '.swift': [
            r'\bprint\s*\(',     # Swift: print(...)
        ],
        '.kt': [
            r'\bprintln\s*\(',   # Kotlin: println(...)
            r'\bprint\s*\(',     # Kotlin: print(...)
        ]
    }
    
    # Get patterns for this file type
    file_patterns = patterns.get(file_ext, [])
    if not file_patterns:
        return 0
    
    total_count = 0
    for pattern in file_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
        total_count += len(matches)
    
    return total_count

def analyze_repository():
    """Analyze all files in the repository"""
    print("🔍 Analyzing files for print statements...")
    print("=" * 60)
    
    # File extensions to analyze
    code_extensions = {'.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.ts', '.jsx', '.tsx'}
    
    results = []
    total_files = 0
    total_prints = 0
    
    # Walk through all files
    for root, dirs, files in os.walk('.'):
        # Skip .git and other hidden directories, but keep .github/scripts
        dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.github']
        
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix.lower()
            
            # Skip the analyzer script itself
            if 'analyze_files.py' in file_path:
                continue
            
            # Only analyze code files
            if file_ext in code_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    print_count = count_print_statements(file_path, content)
                    
                    results.append({
                        'file': file_path,
                        'extension': file_ext,
                        'prints': print_count
                    })
                    
                    total_files += 1
                    total_prints += print_count
                    
                except Exception as e:
                    print(f"⚠️  Error reading {file_path}: {e}")
    
    # Sort results by print count (descending) then by filename
    results.sort(key=lambda x: (-x['prints'], x['file']))
    
    # Display results
    if results:
        print(f"📊 Found {total_files} code files")
        print(f"🖨️  Total print statements: {total_prints}")
        print("\n📋 File Analysis Results:")
        print("-" * 60)
        
        for result in results:
            status = "🔥" if result['prints'] > 5 else "✅" if result['prints'] > 0 else "⚪"
            print(f"{status} {result['file']:<40} | {result['extension']:<6} | {result['prints']:>3} prints")
        
        if total_prints > 0:
            print(f"\n🎯 Files with most print statements:")
            top_files = [r for r in results if r['prints'] > 0][:5]
            for i, result in enumerate(top_files, 1):
                print(f"   {i}. {result['file']} ({result['prints']} prints)")
        
        # Summary statistics
        print(f"\n📈 Summary Statistics:")
        print(f"   • Average prints per file: {total_prints/total_files:.1f}")
        files_with_prints = len([r for r in results if r['prints'] > 0])
        print(f"   • Files with print statements: {files_with_prints}/{total_files}")
        if files_with_prints > 0:
            print(f"   • Avg prints in files with prints: {total_prints/files_with_prints:.1f}")
    else:
        print("ℹ️  No code files found to analyze")

if __name__ == "__main__":
    print("🐍 File Analyzer Script Starting...")
    print(f"📂 Working directory: {os.getcwd()}")
    analyze_repository()
    print("✨ Analysis complete!")