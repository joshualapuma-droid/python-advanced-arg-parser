# Advanced Argument Parser - Intelligent CLI Argument Handling

**Build sophisticated command-line interfaces with auto-completion, validation, and interactive modes beyond standard argparse.**

## What You Get

- `advanced_arg_parser.py` - Main parser with intelligent features
- `arg_parser_examples.py` - Complete usage examples
- `README.md` - Comprehensive documentation
- `ARG_PARSER_README.md` - Additional guides
- MIT License for commercial use

## Key Features

✅ **Intelligent Type Detection** - Automatically detects and converts argument types  
✅ **Advanced Validation** - Custom validators with detailed error messages  
✅ **Auto-completion** - Shell auto-completion for bash/zsh/fish  
✅ **Interactive Mode** - Guided argument input with prompts  
✅ **Configuration Files** - Load/save arguments from JSON/YAML/INI  
✅ **Environment Variables** - Automatic env var integration  
✅ **Rich Help Text** - Colored help with examples  
✅ **Subcommands** - Hierarchical command structure  
✅ **GUI Mode** - Tkinter-based visual argument builder  
✅ **History & Macros** - Command history and saved combinations  
✅ **Plugin System** - Extensible architecture  
✅ **No Dependencies** - Pure Python stdlib (optional: pyyaml, colorama for enhanced features)

## Quick Start

```python
from advanced_arg_parser import AdvancedArgumentParser

# Create parser with intelligent features
parser = AdvancedArgumentParser(
    prog='myapp',
    description='My awesome application'
)

# Add arguments with smart type detection
parser.add_argument('--count', type='auto', default=1,
                   help='Number of items (auto-detects int)')
parser.add_argument('--output', type='path',
                   help='Output file path with validation')
parser.add_argument('--port', type='int', 
                   validator=lambda x: 1024 <= x <= 65535,
                   help='Port number with range validation')

# Enable interactive mode for missing arguments
parser.enable_interactive_mode()

# Parse arguments
args = parser.parse_args()
print(f"Processing {args.count} items...")
```

## Advanced Usage

### Configuration Files

```python
# Load from config file (JSON, YAML, or INI)
parser.load_config('config.json')

# Save current arguments for later
parser.save_config('last_run.json')

# Config auto-discovery from multiple locations
parser.auto_load_config(search_paths=['.', '~/.config', '/etc'])
```

### Custom Validation

```python
# File path validation
parser.add_argument('--config', type='file',
                   exists=True,      # File must exist
                   readable=True,    # Must be readable
                   extensions=['.json', '.yaml'])

# Directory validation
parser.add_argument('--output-dir', type='dir',
                   create=True,      # Create if doesn't exist
                   writable=True)    # Must be writable

# Network validation
parser.add_argument('--api-url', validator='url')
parser.add_argument('--email', validator='email')
parser.add_argument('--ip', validator='ip_address')
```

### Shell Auto-completion

```python
# Enable completion for bash
parser.enable_completion()
parser.generate_bash_completion()

# Or for zsh
parser.generate_zsh_completion()

# Install completion script
parser.install_completion('bash')
```

### GUI Argument Builder

```python
from advanced_arg_parser import ArgumentBuilderGUI

# Visual argument builder
gui = ArgumentBuilderGUI(parser)
gui.run()  # Opens Tkinter interface
```

## Use Cases

1. **Complex CLI Tools** - Build professional command-line applications with rich features
2. **Data Processing Scripts** - Interactive parameter input for data science workflows
3. **DevOps Tools** - Configuration management with file-based argument loading
4. **API Clients** - Validate URLs, endpoints, credentials with built-in validators
5. **Code Generators** - Interactive wizards for scaffolding projects
6. **System Administration** - Scripts with intelligent defaults and validation

## API Reference

### AdvancedArgumentParser

**Main Methods:**
- `add_argument(*args, **kwargs)` - Add argument with enhanced validation
- `parse_args(args=None)` - Parse arguments with auto-completion
- `enable_interactive_mode()` - Prompt for missing required arguments
- `load_config(filename)` - Load arguments from JSON/YAML/INI file
- `save_config(filename)` - Save current configuration
- `enable_completion()` - Enable shell auto-completion
- `add_subparser(name, **kwargs)` - Add subcommand parser

**Enhanced Argument Options:**
- `type='auto'` - Automatic type detection
- `type='file'` - File path with validation (exists, readable, extensions)
- `type='dir'` - Directory path with validation (create, writable)
- `type='path'` - Generic path handling
- `validator=func` - Custom validation function
- `validator='url'` - URL validation
- `validator='email'` - Email validation
- `validator='ip_address'` - IP address validation
- `min_value=n, max_value=n` - Numeric range validation

### ConfigManager

- `load(filename)` - Load config from file (auto-detects format)
- `save(filename, data)` - Save config to file
- `merge(config1, config2)` - Merge multiple configs

### CompletionEngine

- `generate_bash_completion()` - Generate bash completion script
- `generate_zsh_completion()` - Generate zsh completion script
- `install_completion(shell)` - Install completion for shell

## Shopify Product Details

**Product Title:** Advanced Argument Parser - Intelligent CLI Tool Builder  
**Price:** $49  
**Product Type:** Digital Download - Python Library  
**Tags:** python, cli, argparse, command-line, validation, auto-completion, interactive-mode, configuration, argument-parser, developer-tools  
**Short Description:** Build professional command-line interfaces with auto-completion, validation, interactive prompts, and configuration file support.

**SEO Title:** Python Advanced Argument Parser with Auto-completion & Validation  
**Meta Description:** Professional CLI argument parsing beyond argparse. Auto-completion, interactive mode, config files, smart validation. Only $49. Instant download.

## What Customers Get

1. Complete source code (`advanced_arg_parser.py`, `arg_parser_examples.py`)
2. Comprehensive documentation (README.md, ARG_PARSER_README.md)
3. Working code examples demonstrating all features
4. MIT License - use in commercial projects without restrictions
5. Lifetime updates - all future improvements included
6. Email support for integration questions

## System Requirements

- Python 3.8 or higher
- No external dependencies (pure stdlib)
- Optional: `pyyaml` for YAML config support
- Optional: `colorama` for colored output
- Optional: `prompt_toolkit` for enhanced interactive mode
- Works on Windows, macOS, Linux

## Integration Examples

### With Flask/FastAPI

```python
from flask import Flask, request
from advanced_arg_parser import AdvancedArgumentParser

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_command():
    parser = AdvancedArgumentParser()
    # Define arguments...
    try:
        args = parser.parse_args(request.json['command'].split())
        return {'success': True, 'args': vars(args)}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### With Data Science Workflows

```python
# Interactive data processing script
parser = AdvancedArgumentParser()
parser.add_argument('--input', type='file', exists=True, 
                   extensions=['.csv', '.xlsx'])
parser.add_argument('--columns', type='list', 
                   help='Columns to process')
parser.add_argument('--method', choices=['mean', 'median', 'mode'])

parser.enable_interactive_mode()  # Prompt for missing args
args = parser.parse_args()

import pandas as pd
df = pd.read_csv(args.input)
result = df[args.columns].agg(args.method)
```

## Comparison with Standard argparse

| Feature | Standard argparse | Advanced Argument Parser |
|---------|------------------|-------------------------|
| Basic parsing | ✅ | ✅ |
| Type detection | Manual | Automatic |
| File validation | No | ✅ Built-in |
| Interactive mode | No | ✅ |
| Config files | No | ✅ JSON/YAML/INI |
| Auto-completion | No | ✅ Bash/Zsh/Fish |
| GUI builder | No | ✅ Tkinter |
| Custom validators | Limited | ✅ Extensive |
| Environment vars | No | ✅ Auto-integration |
| Subcommands | Basic | ✅ Enhanced |

## License

MIT License - Commercial use allowed, no attribution required.

**Buy Now - $49**

*Instant download after purchase. Build professional CLI tools in minutes!*
