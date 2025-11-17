# Generate ASCII diagram of Python code structure.
Analyzes a Python file and outputs a vertical flow diagram to a markdown file.

## USAGE:
    python generate_code_diagram.py <input_file.py> [OPTIONS]

### BASIC EXAMPLES:
    # Same directory
    python generate_code_diagram.py my_script.py
    
    # Relative path
    python generate_code_diagram.py ../other_folder/script.py
    
    # Absolute path
    python generate_code_diagram.py C:\\Users\\Name\\Documents\\project\\script.py

### CLI OPTIONS:

Input File:

    <input_file.py>
        Path to Python file to analyze (required)
        Supports relative paths, absolute paths, and same directory
        Examples:
            script.py
            ../folder/script.py
            C:\\path\\to\\script.py

Output Options:

    -o, --output <file>
        Specify custom output file path (supports full paths)
        Default: Creates <input_file>_structure.md in same directory as input
        Examples:
            python generate_code_diagram.py script.py -o diagram.md
            python generate_code_diagram.py C:\\code\\script.py -o D:\\docs\\output.md

Diagram Style Options (mutually exclusive):

    -l, --line (DEFAULT)
        Tree-style diagram with Unicode line connectors (┌─, ╔═, ├─, │)
        Best for: Quick overview, terminal viewing
        Example: python generate_code_diagram.py script.py -l
    
    -b, --box
        Nested box diagram with classes as containers (╔═╗, ┌─┐)
        Shows methods inside class boxes with arrows (↓) between elements
        Best for: Understanding class structure and nesting
        Example: python generate_code_diagram.py script.py -b
    
    -a, --ascii-art
        Horizontal flow diagram with ASCII art boxes and connectors
        Uses +---+, [---], |, v, and +----> for visual flow
        Best for: Network-style topology views
        Example: python generate_code_diagram.py script.py -a
    
    -g, --github
        GitHub README optimized format with Mermaid flowchart
        Includes emojis (📋, 🔄, 📦, ⚙️) and component summary
        Renders as interactive diagram on GitHub
        Best for: Documentation, GitHub READMEs
        Example: python generate_code_diagram.py script.py -g

Content Options:

    --include-control-flow
        Include if statements, for loops, and while loops in the diagram
        By default, only functions and classes are shown
        Example: python generate_code_diagram.py script.py --include-control-flow

## COMPLETE EXAMPLES:
    # Basic usage with default line style
    python generate_code_diagram.py my_script.py
    
    # Analyze file in different directory
    python generate_code_diagram.py ../project/main.py
    
    # Box style with control flow
    python generate_code_diagram.py my_script.py -b --include-control-flow
    
    # GitHub style with custom output location
    python generate_code_diagram.py C:\\code\\script.py -g -o D:\\docs\\README_diagram.md
    
    # ASCII art style with relative path
    python generate_code_diagram.py ../src/module.py -a
    
    # Absolute path with custom output in same directory
    python generate_code_diagram.py C:\\Users\\Name\\project\\app.py -o C:\\Users\\Name\\project\\flow.md
