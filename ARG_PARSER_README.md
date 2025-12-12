# Advanced Argument Parser

**Fixes all the arg shit you run into!** 🚀

A robust, intelligent argument parsing system that eliminates common command-line argument headaches.

## Features

- ✅ **Smart Type Inference** - Automatically detects argument types from names
- ✅ **Auto-Generated Help** - Helpful descriptions without manual typing
- ✅ **Environment Variables** - Seamless env var integration
- ✅ **Config File Support** - JSON/YAML config loading
- ✅ **Fuzzy Matching** - Suggests corrections for typos
- ✅ **Subcommands** - Clean subcommand organization
- ✅ **Validation** - Type checking and custom validators
- ✅ **Unicode Elimination** - No more emoji bullshit in arguments! 🇺🇸
- ✅ **Error Recovery** - Helpful error messages and suggestions

## Quick Start

```python
from advanced_arg_parser import ArgumentParser

# Create parser
parser = ArgumentParser("my-tool", "My awesome CLI tool")

# Add arguments (smart defaults!)
parser.add_argument("input", help="Input file")
parser.add_argument("output", help="Output file")
parser.add_argument("verbose", help="Verbose mode")
parser.add_argument("threads", help="Number of threads")

# Parse!
args = parser.parse_args()
```

## Advanced Usage

### Type Inference
The parser automatically infers types from argument names:

```python
parser.add_argument("count", help="Number of items")        # → int
parser.add_argument("rate", help="Compression rate")       # → float
parser.add_argument("enable-logging", help="Enable logs")  # → bool
parser.add_argument("config-file", help="Config path")     # → str
```

### Environment Variables
Arguments automatically map to environment variables:

```python
# --input-file → MY_TOOL_INPUT_FILE env var
parser.add_argument("input-file", help="Input file")
```

### Config Files
Load defaults from JSON/YAML files:

```python
parser.add_config_file("tool_config.json")
parser.add_config_file("~/.tool_config.json")
```

### Subcommands
Organize complex tools with subcommands:

```python
def build_parser(subparser):
    subparser.add_argument("target", help="Build target")

parser.add_subcommand("build", build_parser, "Build the project")
```

### Quick Parse
Simple argument parsing for basic tools:

```python
from advanced_arg_parser import quick_parse

args = quick_parse({
    'input': {'type': str, 'help': 'Input file'},
    'verbose': {'type': bool, 'help': 'Verbose mode'}
})
```

## Common Problems Solved

### ❌ Before (Standard argparse)
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True, help='Input file path')
parser.add_argument('--count', type=int, default=0, help='Number of items')
parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('--rate', type=float, default=1.0, help='Processing rate')

# Manual error handling, no suggestions, tedious setup
```

### ✅ After (Advanced Argument Parser)
```python
from advanced_arg_parser import ArgumentParser

parser = ArgumentParser("my-tool", "Process files intelligently")
parser.add_argument("input", help="Input file path")
parser.add_argument("count", help="Number of items")
parser.add_argument("verbose", help="Enable verbose output")
parser.add_argument("rate", help="Processing rate")

args = parser.parse_args()  # That's it!
```

## Error Handling

The parser provides intelligent error handling:

```
$ my-tool --inputt file.txt
usage: my-tool [-h] --input INPUT ...
my-tool: error: the following arguments are required: --input

Suggestions:
  - Check argument names and try --help for usage
  - Use quotes around arguments with spaces
  - Ensure required arguments are provided
  - Did you mean: --input?
```

## Integration

Drop `advanced_arg_parser.py` into your project and import:

```python
from advanced_arg_parser import ArgumentParser, quick_parse
```

## Testing

Run the comprehensive test suite:

```bash
python test_arg_parser.py
```

See usage examples:

```bash
python arg_parser_examples.py
```

## No More Arg Shit!

- ❌ Manual type specification
- ❌ Boilerplate argparse code
- ❌ Cryptic error messages
- ❌ No environment variable support
- ❌ Manual help text writing
- ❌ No config file integration
- ❌ Typos cause silent failures
- ❌ Unicode and emoji argument problems

- ✅ Smart type inference
- ✅ Auto-generated help
- ✅ Environment variables
- ✅ Config file support
- ✅ Fuzzy argument matching
- ✅ Helpful error suggestions
- ✅ Subcommand functionality
- ✅ Unicode elimination (emoji-free arguments!)

**Your argument parsing just got 10x smarter!** 🧠✨