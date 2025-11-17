#!/usr/bin/env python3
import ast
import argparse
import sys
from pathlib import Path


class CodeStructureAnalyzer(ast.NodeVisitor):
    """Analyzes Python code structure using AST."""
    
    def __init__(self, include_control_flow=False):
        self.structure = []
        self.current_level = 0
        self.include_control_flow = include_control_flow
        
    def visit_FunctionDef(self, node):
        """Visit function definitions."""
        self.structure.append({
            'type': 'function',
            'name': node.name,
            'level': self.current_level,
            'lineno': node.lineno
        })
        self.current_level += 1
        self.generic_visit(node)
        self.current_level -= 1
        
    def visit_ClassDef(self, node):
        """Visit class definitions."""
        self.structure.append({
            'type': 'class',
            'name': node.name,
            'level': self.current_level,
            'lineno': node.lineno
        })
        self.current_level += 1
        self.generic_visit(node)
        self.current_level -= 1
        
    def visit_If(self, node):
        """Visit if statements."""
        if self.include_control_flow:
            self.structure.append({
                'type': 'conditional',
                'name': 'if statement',
                'level': self.current_level,
                'lineno': node.lineno
            })
        self.generic_visit(node)
        
    def visit_For(self, node):
        """Visit for loops."""
        if self.include_control_flow:
            self.structure.append({
                'type': 'loop',
                'name': 'for loop',
                'level': self.current_level,
                'lineno': node.lineno
            })
        self.generic_visit(node)
        
    def visit_While(self, node):
        """Visit while loops."""
        if self.include_control_flow:
            self.structure.append({
                'type': 'loop',
                'name': 'while loop',
                'level': self.current_level,
                'lineno': node.lineno
            })
        self.generic_visit(node)


def generate_line_diagram(structure, filename):
    """Generate line-style ASCII diagram from structure."""
    lines = []
    lines.append(f"# Code Structure: {filename}")
    lines.append("")
    lines.append("```")
    
    if not structure:
        lines.append("(No structure detected)")
        lines.append("```")
        return "\n".join(lines)
    
    for i, item in enumerate(structure):
        indent = "  " * item['level']
        
        # Determine symbol based on type
        if item['type'] == 'function':
            symbol = "┌─"
            name = f"[FUNCTION] {item['name']}()"
        elif item['type'] == 'class':
            symbol = "╔═"
            name = f"[CLASS] {item['name']}"
        elif item['type'] == 'conditional':
            symbol = "├─"
            name = f"[IF] {item['name']}"
        elif item['type'] == 'loop':
            symbol = "├─"
            name = f"[LOOP] {item['name']}"
        else:
            symbol = "├─"
            name = item['name']
        
        # Add connector from previous item if needed
        if i > 0:
            prev_level = structure[i-1]['level']
            curr_level = item['level']
            
            if curr_level <= prev_level:
                # Going back up, add vertical connectors
                for level in range(curr_level, prev_level):
                    lines.append("  " * level + "│")
        
        lines.append(f"{indent}{symbol} {name}")
    
    lines.append("```")
    return "\n".join(lines)


def generate_ascii_art_diagram(structure, filename):
    """Generate ASCII art style diagram with horizontal flow."""
    lines = []
    lines.append(f"# Code Structure: {filename}")
    lines.append("")
    lines.append("```")
    
    if not structure:
        lines.append("(No structure detected)")
        lines.append("```")
        return "\n".join(lines)
    
    lines.append("Code Flow:")
    lines.append("-" * 60)
    lines.append("")
    
    # Group items by level
    max_level = max(item['level'] for item in structure)
    
    for i, item in enumerate(structure):
        level = item['level']
        
        # Determine label
        if item['type'] == 'function':
            label = f"{item['name']}()"
        elif item['type'] == 'class':
            label = f"CLASS: {item['name']}"
        elif item['type'] == 'conditional':
            label = f"IF"
        elif item['type'] == 'loop':
            label = f"LOOP"
        else:
            label = item['name']
        
        # Create box
        box_width = len(label) + 2
        indent = " " * (level * 4)
        
        # Add connection line from previous item
        if i > 0:
            prev_level = structure[i-1]['level']
            
            if level == prev_level:
                # Same level - vertical arrow
                lines.append(f"{indent}  |")
                lines.append(f"{indent}  v")
            elif level > prev_level:
                # Going deeper - show nesting
                lines.append(f"{indent}  |")
                lines.append(f"{indent}  +---->")
            else:
                # Going back up
                lines.append(f"{indent}  |")
        
        # Draw the box
        if item['type'] == 'class':
            lines.append(f"{indent}+{'-' * box_width}+")
            lines.append(f"{indent}| {label} |")
            lines.append(f"{indent}+{'-' * box_width}+")
            
            # Check if class has methods
            if i < len(structure) - 1 and structure[i+1]['level'] > level:
                lines.append(f"{indent}| (contains methods below)")
        else:
            lines.append(f"{indent}[{'-' * box_width}]")
            lines.append(f"{indent}| {label} |")
            lines.append(f"{indent}[{'-' * box_width}]")
    
    lines.append("")
    lines.append("-" * 60)
    lines.append("```")
    return "\n".join(lines)


def generate_github_diagram(structure, filename):
    """Generate GitHub README optimized diagram with emojis and clean formatting."""
    lines = []
    lines.append(f"## 📋 Code Structure: `{filename}`")
    lines.append("")
    
    if not structure:
        lines.append("```")
        lines.append("(No structure detected)")
        lines.append("```")
        return "\n".join(lines)
    
    # Separate top-level items from nested ones
    lines.append("### 🔄 Execution Flow")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph TD")
    
    # First pass: Create node IDs and definitions
    node_id = 0
    node_map = {}
    node_definitions = []
    methods_per_row = 4
    
    for i, item in enumerate(structure):
        current_id = f"N{node_id}"
        node_map[i] = current_id
        
        # Determine node style and label - use quoted strings for Mermaid compatibility
        if item['type'] == 'function':
            label = f"{item['name']}()"
            node_style = f'{current_id}["{label}"]'
        elif item['type'] == 'class':
            label = f"📦 {item['name']}"
            node_style = f'{current_id}[/"{label}"/]'
        elif item['type'] == 'conditional':
            label = "Conditional"
            node_style = f'{current_id}{{"{label}"}}'
        elif item['type'] == 'loop':
            label = "Loop"
            node_style = f'{current_id}{{"{label}"}}'
        else:
            label = item['name']
            node_style = f'{current_id}["{label}"]'
        
        node_definitions.append(f"    {node_style}")
        node_id += 1
    
    # Add all node definitions first
    lines.extend(node_definitions)
    
    # Second pass: Create connections
    i = 0
    while i < len(structure):
        item = structure[i]
        current_id = node_map[i]
        
        # Handle connections based on structure
        if item['type'] == 'class':
            # Connect class to previous top-level item in sequential flow
            if item['level'] == 0 and i > 0:
                for j in range(i - 1, -1, -1):
                    if structure[j]['level'] == 0:
                        prev_top_id = node_map[j]
                        lines.append(f"    {prev_top_id} --> {current_id}")
                        break
            
            # Find all methods in this class
            class_methods = []
            j = i + 1
            while j < len(structure) and structure[j]['level'] > item['level']:
                if structure[j]['type'] == 'function' and structure[j]['level'] == item['level'] + 1:
                    class_methods.append(j)
                j += 1
            
            # Connect methods in rows of 4
            if class_methods:
                for row_start in range(0, len(class_methods), methods_per_row):
                    row_methods = class_methods[row_start:row_start + methods_per_row]
                    
                    # Connect class to first method in row
                    first_method_idx = row_methods[0]
                    first_method_id = node_map[first_method_idx]
                    lines.append(f"    {current_id} --> {first_method_id}")
                    
                    # Connect methods horizontally in this row
                    for k in range(len(row_methods) - 1):
                        method_idx = row_methods[k]
                        next_method_idx = row_methods[k + 1]
                        method_id = node_map[method_idx]
                        next_method_id = node_map[next_method_idx]
                        lines.append(f"    {method_id} -.-> {next_method_id}")
            
            # Connect class to next top-level item in sequential flow
            if item['level'] == 0:
                for j in range(i + 1, len(structure)):
                    if structure[j]['level'] == 0:
                        next_top_id = node_map[j]
                        lines.append(f"    {current_id} --> {next_top_id}")
                        break
        
        elif item['level'] == 0 and i > 0 and item['type'] in ['function', 'conditional', 'loop']:
            # Top-level function or control flow - connect to previous top-level item
            # But skip if previous item is a class (already connected)
            prev_is_class = False
            for j in range(i - 1, -1, -1):
                if structure[j]['level'] == 0:
                    if structure[j]['type'] == 'class':
                        prev_is_class = True
                    break
            
            if not prev_is_class:
                for j in range(i - 1, -1, -1):
                    if structure[j]['level'] == 0 and structure[j]['type'] in ['function', 'conditional', 'loop']:
                        prev_top_id = node_map[j]
                        lines.append(f"    {prev_top_id} --> {current_id}")
                        break
        
        i += 1
    
    lines.append("```")
    lines.append("")
    
    # Add text-based summary
    lines.append("### 📚 Components")
    lines.append("")
    
    # Group by type
    classes = [item for item in structure if item['type'] == 'class' and item['level'] == 0]
    functions = [item for item in structure if item['type'] == 'function' and item['level'] == 0]
    
    if classes:
        lines.append("#### 📦 Classes")
        for cls in classes:
            # Find where this class's methods end
            class_idx = structure.index(cls)
            class_methods = []
            for j in range(class_idx + 1, len(structure)):
                if structure[j]['level'] <= cls['level']:
                    break
                if structure[j]['type'] == 'function' and structure[j]['level'] == cls['level'] + 1:
                    class_methods.append(structure[j]['name'])
            
            if class_methods:
                lines.append(f"- **`{cls['name']}`** - Contains {len(class_methods)} method(s)")
                for method in class_methods:  # Show all methods
                    lines.append(f"  - `{method}()`")
            else:
                lines.append(f"- **`{cls['name']}`**")
        lines.append("")
    
    if functions:
        lines.append("#### ⚙️ Functions")
        for func in functions:
            lines.append(f"- `{func['name']}()`")
        lines.append("")
    
    return "\n".join(lines)


def generate_box_diagram(structure, filename):
    """Generate box-style ASCII diagram with proper nesting."""
    lines = []
    lines.append(f"# Code Structure: {filename}")
    lines.append("")
    lines.append("```")
    
    if not structure:
        lines.append("(No structure detected)")
        lines.append("```")
        return "\n".join(lines)
    
    open_containers = []  # Track open class/function containers
    
    for i, item in enumerate(structure):
        indent = "  " * item['level']
        curr_level = item['level']
        
        # Determine label based on type
        if item['type'] == 'function':
            label = f"FUNCTION: {item['name']}()"
        elif item['type'] == 'class':
            label = f"CLASS: {item['name']}"
        elif item['type'] == 'conditional':
            label = f"IF: {item['name']}"
        elif item['type'] == 'loop':
            label = f"LOOP: {item['name']}"
        else:
            label = item['name']
        
        box_width = len(label) + 2
        
        # Check if we need to close containers
        if i > 0:
            prev_level = structure[i-1]['level']
            
            # Close containers when going back to same or lower level
            if curr_level <= prev_level:
                # Close containers
                while open_containers and open_containers[-1]['level'] >= curr_level:
                    container = open_containers.pop()
                    container_indent = "  " * container['level']
                    lines.append(f"{container_indent}╚{'═' * container['width']}╝")
                
                # Add arrow between same-level items
                if curr_level == prev_level:
                    lines.append(f"{indent}  ↓")
            else:
                # Going deeper - add arrow
                lines.append(f"{indent}  ↓")
        
        # Check if this is a container (class) or if next item is nested
        is_container = False
        if item['type'] == 'class':
            is_container = True
        elif i < len(structure) - 1 and structure[i+1]['level'] > curr_level:
            is_container = True
        
        if is_container and item['type'] == 'class':
            # Draw class as a container with double lines
            lines.append(f"{indent}╔{'═' * box_width}╗")
            lines.append(f"{indent}║ {label} ║")
            lines.append(f"{indent}╠{'═' * box_width}╣")
            open_containers.append({'level': curr_level, 'width': box_width})
        else:
            # Draw regular box
            lines.append(f"{indent}┌{'─' * box_width}┐")
            lines.append(f"{indent}│ {label} │")
            lines.append(f"{indent}└{'─' * box_width}┘")
    
    # Close any remaining open containers
    while open_containers:
        container = open_containers.pop()
        container_indent = "  " * container['level']
        lines.append(f"{container_indent}╚{'═' * container['width']}╝")
    
    lines.append("```")
    return "\n".join(lines)


def analyze_python_file(input_file, include_control_flow=False):
    """Analyze Python file and extract structure."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source, filename=input_file)
        analyzer = CodeStructureAnalyzer(include_control_flow=include_control_flow)
        analyzer.visit(tree)
        
        return analyzer.structure
    except SyntaxError as e:
        print(f"Syntax error in {input_file}: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error analyzing {input_file}: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(
        description='Generate ASCII diagram of Python code structure'
    )
    parser.add_argument(
        'input_file',
        help='Input Python file to analyze'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output markdown file (default: <input>_structure.md)',
        default=None
    )
    parser.add_argument(
        '--include-control-flow',
        action='store_true',
        help='Include if statements and loops in the diagram'
    )
    
    style_group = parser.add_mutually_exclusive_group()
    style_group.add_argument(
        '-l', '--line',
        action='store_true',
        help='Use line-style diagram (default)'
    )
    style_group.add_argument(
        '-b', '--box',
        action='store_true',
        help='Use box-style diagram with nested boxes'
    )
    style_group.add_argument(
        '-a', '--ascii-art',
        action='store_true',
        help='Use ASCII art style with horizontal flow'
    )
    style_group.add_argument(
        '-g', '--github',
        action='store_true',
        help='Use GitHub README optimized format with Mermaid diagram'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    if not input_path.suffix == '.py':
        print(f"Warning: '{args.input_file}' is not a .py file", file=sys.stderr)
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_name(f"{input_path.stem}_structure.md")
    
    # Analyze the file
    print(f"Analyzing {input_path}...")
    structure = analyze_python_file(input_path, include_control_flow=args.include_control_flow)
    
    # Generate diagram based on style
    if args.box:
        diagram = generate_box_diagram(structure, input_path.name)
    elif args.ascii_art:
        diagram = generate_ascii_art_diagram(structure, input_path.name)
    elif args.github:
        diagram = generate_github_diagram(structure, input_path.name)
    else:
        diagram = generate_line_diagram(structure, input_path.name)
    
    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(diagram)
    
    print(f"Diagram saved to {output_path}")
    print(f"Found {len(structure)} structural elements")


if __name__ == '__main__':
    main()
