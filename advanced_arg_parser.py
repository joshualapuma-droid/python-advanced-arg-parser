#!/usr/bin/env python3
"""
Advanced Argument Parser - Fixes all the arg shit!
===============================================

A robust, flexible argument parsing system that handles:
- Type validation and conversion
- Default values with smart inference
- Required argument enforcement
- Help generation
- Error handling with suggestions
- Environment variable integration
- Config file support
- Subcommand handling
- Unicode elimination for maximum compatibility
"""

import argparse
import json
import os
import re
import sys
import unicodedata
import warnings
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

# Try to import Unicode elimination libraries
try:
    import unidecode

    UNIDECODE_AVAILABLE = True
except ImportError:
    UNIDECODE_AVAILABLE = False

try:
    import emoji

    EMOJI_AVAILABLE = True
except ImportError:
    EMOJI_AVAILABLE = False

try:
    import ftfy

    FTFY_AVAILABLE = True
except ImportError:
    FTFY_AVAILABLE = False


class UnicodeEliminator:
    """
    Maximum Unicode and Emoji Elimination System
    Permanently removes all Unicode bullshit and emoji errors
    """

    def __init__(self, aggressive: bool = True, ascii_only: bool = True):
        """
        Initialize the Unicode Eliminator

        Args:
            aggressive: If True, remove ALL non-ASCII characters
            ascii_only: If True, convert everything to pure ASCII
        """
        self.aggressive = aggressive
        self.ascii_only = ascii_only

        # Compile regex patterns for maximum efficiency
        self.emoji_pattern = re.compile(
            "["
            "\U0001f600-\U0001f64f"  # emoticons
            "\U0001f300-\U0001f5ff"  # symbols & pictographs
            "\U0001f680-\U0001f6ff"  # transport & map symbols
            "\U0001f1e0-\U0001f1ff"  # flags (iOS)
            "\U00002700-\U000027bf"  # dingbats
            "\U0001f926-\U0001f937"  # gestures
            "\U00010000-\U0010ffff"  # other unicode
            "\u2640-\u2642"  # gender symbols
            "\u2600-\u2b55"  # misc symbols
            "\u200d"  # zero width joiner
            "\u23cf"  # eject symbol
            "\u23e9"  # fast forward
            "\u231a"  # watch
            "\ufe0f"  # variation selector
            "\u3030"  # wavy dash
            "]+",
            flags=re.UNICODE,
        )

    def eliminate_unicode(self, text: Union[str, Any]) -> Union[str, Any]:
        """
        Maximum Unicode elimination - removes all emoji and Unicode bullshit
        """
        if not isinstance(text, str):
            return text

        # Step 1: Fix common encoding issues
        if FTFY_AVAILABLE:
            text = ftfy.fix_text(text)

        # Step 2: Remove emoji
        if EMOJI_AVAILABLE:
            text = emoji.replace_emoji(text, replace="")
        else:
            text = self.emoji_pattern.sub("", text)

        # Step 3: Convert to ASCII
        if UNIDECODE_AVAILABLE and self.ascii_only:
            text = unidecode.unidecode(text)
        elif self.aggressive:
            text = (
                unicodedata.normalize("NFKD", text)
                .encode("ascii", "ignore")
                .decode("ascii")
            )

        # Step 4: Clean up extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename by removing Unicode and special characters
        """
        clean_name = self.eliminate_unicode(filename)
        clean_name = re.sub(r'[<>:"/\\|?*]', "", clean_name)
        clean_name = re.sub(r"[^a-zA-Z0-9._-]", "_", clean_name)
        clean_name = re.sub(r"_+", "_", clean_name).strip("_")
        return clean_name or "file"


# Global Unicode Eliminator instance
_unicode_eliminator = UnicodeEliminator(aggressive=True, ascii_only=True)


def eliminate_unicode_maximum(text: Union[str, Any]) -> Union[str, Any]:
    """
    Maximum Unicode elimination function - use this everywhere!
    Eliminates all emoji and Unicode bullshit from arguments and text
    """
    return _unicode_eliminator.eliminate_unicode(text)


def sanitize_filename_maximum(filename: str) -> str:
    """
    Maximum filename sanitization with Unicode elimination
    """
    return _unicode_eliminator.sanitize_filename(filename)


class ArgumentParser:
    """
    Advanced argument parser that fixes all the common arg parsing problems.
    Now with Unicode elimination for maximum compatibility and emoji-free operation!
    """

    def __init__(
        self,
        program_name: str = None,
        description: str = None,
        unicode_safe: bool = True,
    ):
        self.program_name = program_name or Path(sys.argv[0]).stem
        self.description = description or f"{self.program_name} - Advanced CLI Tool"
        self.args_definitions = {}
        self.subcommands = {}
        self.global_args = {}
        self.config_files = []
        self.env_prefix = self.program_name.upper().replace("-", "_")
        self.unicode_safe = unicode_safe  # Enable Unicode elimination

    def add_argument(self, name: str, **kwargs):
        """
        Add an argument with smart defaults and validation.

        Args:
            name: Argument name (with or without --)
            **kwargs: Standard argparse arguments plus enhancements:
                - type: Auto-detected if not specified
                - default: Smart defaults based on type
                - required: Auto-detected for critical args
                - help: Auto-generated if not provided
                - env_var: Environment variable name
                - config_key: Config file key
        """
        # Normalize name
        if not name.startswith("--"):
            name = f"--{name}"

        # Smart type detection
        if "type" not in kwargs:
            kwargs["type"] = self._infer_type(name, kwargs.get("default"))

        # Smart defaults
        if "default" not in kwargs and kwargs.get("type") != bool:
            kwargs["default"] = self._get_smart_default(kwargs["type"])

        # Smart required detection
        if "required" not in kwargs:
            kwargs["required"] = self._is_required_arg(name)

        # Smart help
        if "help" not in kwargs:
            kwargs["help"] = self._generate_help_text(name, kwargs)

        # Store env var mapping
        if "env_var" not in kwargs:
            kwargs["env_var"] = (
                f"{self.env_prefix}_{name[2:].upper().replace('-', '_')}"
            )

        self.args_definitions[name] = kwargs

    def add_subcommand(self, name: str, parser_func: Callable, help_text: str = None):
        """
        Add a subcommand with its own parser function.

        Args:
            name: Subcommand name
            parser_func: Function that configures subcommand arguments
            help_text: Help description
        """
        self.subcommands[name] = {
            "func": parser_func,
            "help": help_text or f"Run {name} subcommand",
        }

    def add_config_file(self, path: Union[str, Path]):
        """Add a config file to load defaults from."""
        self.config_files.append(Path(path))

    def set_env_prefix(self, prefix: str):
        """Set environment variable prefix."""
        self.env_prefix = prefix

    def _infer_type(self, name: str, default_value) -> type:
        """Infer argument type from name and default."""
        if default_value is not None:
            return type(default_value)

        name_lower = name.lower()

        # Type inference from name patterns
        if any(
            word in name_lower
            for word in ["count", "number", "size", "port", "timeout"]
        ):
            return int
        elif any(word in name_lower for word in ["rate", "factor", "ratio"]):
            return float
        elif any(
            word in name_lower
            for word in ["enable", "disable", "verbose", "quiet", "debug"]
        ):
            return bool
        elif any(
            word in name_lower for word in ["file", "path", "dir", "output", "input"]
        ):
            return str
        else:
            return str

    def _get_smart_default(self, arg_type: type) -> Any:
        """Get smart defaults based on type."""
        defaults = {int: 0, float: 0.0, bool: False, str: "", list: [], dict: {}}
        return defaults.get(arg_type, None)

    def _is_required_arg(self, name: str) -> bool:
        """Determine if an argument should be required."""
        required_patterns = [
            "input",
            "file",
            "source",
            "target",
            "destination",
            "host",
            "server",
            "database",
            "username",
            "password",
        ]
        return any(pattern in name.lower() for pattern in required_patterns)

    def _generate_help_text(self, name: str, kwargs: dict) -> str:
        """Generate helpful help text."""
        arg_type = kwargs.get("type", str)
        default = kwargs.get("default")

        base_name = name[2:].replace("-", " ").title()

        if arg_type == bool:
            return f"Enable or disable {base_name.lower()}"
        elif arg_type == int:
            return f"Set {base_name.lower()} (integer)"
        elif arg_type == float:
            return f"Set {base_name.lower()} (decimal)"
        else:
            help_text = f"Specify {base_name.lower()}"
            if default:
                help_text += f" (default: {default})"
            return help_text

    def _load_config_defaults(self) -> Dict[str, Any]:
        """Load defaults from config files."""
        defaults = {}

        for config_file in self.config_files:
            if config_file.exists():
                try:
                    if config_file.suffix == ".json":
                        with open(config_file, "r") as f:
                            config = json.load(f)
                            defaults.update(config)
                    elif config_file.suffix in [".yaml", ".yml"]:
                        try:
                            import yaml

                            with open(config_file, "r") as f:
                                config = yaml.safe_load(f)
                                defaults.update(config)
                        except ImportError:
                            pass  # YAML not available
                except Exception:
                    pass  # Config file error, skip

        return defaults

    def _load_env_defaults(self) -> Dict[str, Any]:
        """Load defaults from environment variables."""
        defaults = {}

        for arg_name, arg_config in self.args_definitions.items():
            env_var = arg_config.get("env_var")
            if env_var and env_var in os.environ:
                try:
                    value = os.environ[env_var]
                    arg_type = arg_config.get("type", str)

                    # Type conversion
                    if arg_type == bool:
                        defaults[arg_name] = value.lower() in ("true", "1", "yes", "on")
                    elif arg_type == int:
                        defaults[arg_name] = int(value)
                    elif arg_type == float:
                        defaults[arg_name] = float(value)
                    else:
                        defaults[arg_name] = value
                except ValueError:
                    pass  # Invalid env var value, skip

        return defaults

    def parse_args(self, args: List[str] = None) -> argparse.Namespace:
        """
        Parse arguments with all the fixes applied.
        Now with Unicode elimination for maximum compatibility and emoji-free operation!

        Args:
            args: Arguments to parse (default: sys.argv[1:])

        Returns:
            Parsed arguments namespace (Unicode-safe!)
        """
        if args is None:
            args = sys.argv[1:]

        # Apply Unicode elimination to all arguments if enabled
        if self.unicode_safe:
            args = [
                eliminate_unicode_maximum(arg) if isinstance(arg, str) else arg
                for arg in args
            ]

        # Create parser
        parser = argparse.ArgumentParser(
            prog=self.program_name,
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Add subcommands if any
        if self.subcommands:
            subparsers = parser.add_subparsers(
                dest="subcommand", help="Available subcommands"
            )

            for sub_name, sub_config in self.subcommands.items():
                subparser = subparsers.add_parser(sub_name, help=sub_config["help"])
                # Call subcommand parser function
                sub_config["func"](subparser)

        # Load defaults from config and env
        config_defaults = self._load_config_defaults()
        env_defaults = self._load_env_defaults()

        # Add arguments
        for arg_name, arg_config in self.args_definitions.items():
            # Merge defaults (config -> env -> defined default)
            default_value = arg_config.get("default")
            if arg_name in config_defaults:
                default_value = config_defaults[arg_name]
            if arg_name in env_defaults:
                default_value = env_defaults[arg_name]

            # Create argument config (filter out custom parameters)
            arg_kwargs = arg_config.copy()
            arg_kwargs["default"] = default_value

            # Remove custom parameters that argparse doesn't understand
            custom_params = ["env_var", "config_key", "validator"]
            for param in custom_params:
                arg_kwargs.pop(param, None)

            # Handle boolean flags
            if arg_kwargs.get("type") == bool and not arg_kwargs.get("action"):
                arg_kwargs["action"] = "store_true"
                # Remove type for boolean actions
                arg_kwargs.pop("type", None)

            parser.add_argument(arg_name, **arg_kwargs)

        # Parse with error handling
        try:
            parsed_args = parser.parse_args(args)

            # Validate required args
            self._validate_args(parsed_args)

            return parsed_args

        except SystemExit as e:
            # Provide helpful error messages
            if len(args) > 0:
                self._suggest_corrections(args)
            raise e

    def _validate_args(self, args: argparse.Namespace):
        """Validate parsed arguments with Unicode safety."""
        errors = []

        for arg_name, arg_config in self.args_definitions.items():
            attr_name = arg_name[2:].replace("-", "_")
            value = getattr(args, attr_name, None)

            # Apply Unicode elimination to string values if enabled
            if self.unicode_safe and isinstance(value, str):
                value = eliminate_unicode_maximum(value)
                setattr(args, attr_name, value)

            # Type validation
            expected_type = arg_config.get("type")
            if expected_type and value is not None:
                if not isinstance(value, expected_type):
                    try:
                        # Try conversion
                        converted = expected_type(value)
                        setattr(args, attr_name, converted)
                    except (ValueError, TypeError):
                        errors.append(
                            f"{arg_name}: Expected {expected_type.__name__}, got {type(value).__name__}"
                        )

            # Custom validation
            validator = arg_config.get("validator")
            if validator and callable(validator):
                try:
                    validator(value)
                except Exception as e:
                    errors.append(f"{arg_name}: {e}")

        if errors:
            print("Argument validation errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)

    def _suggest_corrections(self, args: List[str]):
        """Suggest corrections for invalid arguments."""
        print("\nSuggestions:")
        print("  - Check argument names and try --help for usage")
        print("  - Use quotes around arguments with spaces")
        print("  - Ensure required arguments are provided")

        # Find similar argument names
        defined_args = [name for name in self.args_definitions.keys()]
        for arg in args:
            if arg.startswith("--"):
                suggestions = self._find_similar_args(arg, defined_args)
                if suggestions:
                    print(f"  - Did you mean: {', '.join(suggestions)}?")

    def _find_similar_args(self, arg: str, candidates: List[str]) -> List[str]:
        """Find similar argument names using fuzzy matching."""
        import difflib

        # Remove -- prefix for comparison
        arg_clean = arg[2:] if arg.startswith("--") else arg
        candidates_clean = [c[2:] if c.startswith("--") else c for c in candidates]

        # Find close matches
        matches = difflib.get_close_matches(
            arg_clean, candidates_clean, n=3, cutoff=0.6
        )
        return [f"--{match}" for match in matches]

    def get_help_text(self) -> str:
        """Get formatted help text."""
        parser = argparse.ArgumentParser(
            prog=self.program_name,
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Add a dummy argument to force help formatting
        parser.add_argument(
            "--help-text", help="Show this help message", action="store_true"
        )

        return parser.format_help()


# Convenience functions
def create_parser(program_name: str = None, description: str = None) -> ArgumentParser:
    """Create a new argument parser instance."""
    return ArgumentParser(program_name, description)


def quick_parse(
    args_dict: Dict[str, Dict], program_name: str = None, unicode_safe: bool = True
) -> argparse.Namespace:
    """
    Quick argument parsing for simple cases.
    Now with Unicode safety enabled by default!

    Args:
        args_dict: Dict of arg_name -> arg_config
        program_name: Program name
        unicode_safe: Enable Unicode elimination (default: True)

    Example:
        args = quick_parse({
            'input': {'type': str, 'help': 'Input file'},
            'verbose': {'type': bool, 'help': 'Verbose output'}
        })
    """
    parser = ArgumentParser(program_name, unicode_safe=unicode_safe)
    for name, config in args_dict.items():
        parser.add_argument(name, **config)
    return parser.parse_args()


# Example usage and testing
if __name__ == "__main__":
    print("🔧 Advanced Argument Parser - Fixes All Arg Shit!")
    print("=" * 55)

    # Example parser setup
    parser = ArgumentParser("my-tool", "Example tool with fixed argument parsing")

    # Add some common arguments
    parser.add_argument("input", type=str, help="Input file path")
    parser.add_argument("output", type=str, help="Output file path")
    parser.add_argument("count", type=int, help="Number of items to process")
    parser.add_argument("verbose", type=bool, help="Enable verbose output")
    parser.add_argument("rate", type=float, help="Processing rate")

    # Test parsing
    test_args = [
        "--input",
        "test.txt",
        "--output",
        "out.txt",
        "--count",
        "42",
        "--verbose",
        "--rate",
        "3.14",
    ]

    try:
        args = parser.parse_args(test_args)
        print("✅ Parsing successful!")
        print(f"Input: {args.input}")
        print(f"Output: {args.output}")
        print(f"Count: {args.count}")
        print(f"Verbose: {args.verbose}")
        print(f"Rate: {args.rate}")
    except SystemExit:
        print("❌ Parsing failed - check the suggestions above")

    print("\n🎯 Key Features:")
    print("  ✅ Smart type inference")
    print("  ✅ Auto-generated help text")
    print("  ✅ Environment variable support")
    print("  ✅ Config file integration")
    print("  ✅ Fuzzy argument matching")
    print("  ✅ Unicode elimination (no more emoji bullshit!)")
    print("  ✅ Comprehensive error handling")
    print("  ✅ Subcommand support")
    print("  ✅ Validation and conversion")
