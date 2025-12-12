#!/usr/bin/env python3
"""
Example: Using Advanced Argument Parser in Your Projects
========================================================

This shows how to integrate the argument parser into your tools
to eliminate all the common argument parsing headaches.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from advanced_arg_parser import ArgumentParser


def create_file_processor():
    """Example: File processing tool with robust argument parsing."""

    parser = ArgumentParser(
        "file-processor", "Process files with various transformations and options"
    )

    # Add arguments with smart defaults and type inference
    parser.add_argument("input", help="Input file to process")
    parser.add_argument("output", help="Output file (optional)", required=False)
    parser.add_argument("format", help="Output format (json, xml, csv)", required=False)
    parser.add_argument("compress", type=bool, help="Enable compression")
    parser.add_argument("threads", help="Number of processing threads", required=False)
    parser.add_argument("verbose", type=bool, help="Enable verbose output")
    parser.add_argument("config", help="Configuration file", required=False)

    # Add config file support
    parser.add_config_file("file_processor.json")
    parser.add_config_file("~/.file_processor.json")

    return parser


def create_data_analyzer():
    """Example: Data analysis tool."""

    parser = ArgumentParser(
        "data-analyzer", "Analyze datasets with statistical and ML methods"
    )

    # Dataset arguments
    parser.add_argument("dataset", help="Path to dataset file")
    parser.add_argument("target", help="Target column for analysis")

    # Analysis options
    parser.add_argument(
        "method", help="Analysis method (stats, ml, viz)", required=False
    )
    parser.add_argument(
        "output-dir", help="Output directory for results", required=False
    )
    parser.add_argument("cross-validation", type=bool, help="Enable cross-validation")
    parser.add_argument(
        "feature-selection", type=bool, help="Enable automatic feature selection"
    )

    # Performance options
    parser.add_argument("parallel", type=bool, help="Enable parallel processing")
    parser.add_argument("memory-limit", help="Memory limit in GB", required=False)
    parser.add_argument("timeout", help="Analysis timeout in minutes", required=False)

    return parser


def create_web_scraper():
    """Example: Web scraping tool with subcommands."""

    parser = ArgumentParser(
        "web-scraper", "Scrape websites with various extraction methods"
    )

    # Global options
    parser.add_argument("verbose", help="Enable verbose output")
    parser.add_argument("delay", help="Delay between requests")
    parser.add_argument("user-agent", help="Custom user agent string", required=False)

    # Subcommands for different scraping tasks
    def crawl_parser(subparser):
        subparser.add_argument("url", help="Starting URL to crawl")
        subparser.add_argument("depth", help="Crawl depth")
        subparser.add_argument("output", help="Output file for crawled data")

    def extract_parser(subparser):
        subparser.add_argument("url", help="URL to extract from")
        subparser.add_argument("selectors", help="CSS selectors for extraction")
        subparser.add_argument("format", help="Output format (json, csv)")

    def monitor_parser(subparser):
        subparser.add_argument("url", help="URL to monitor")
        subparser.add_argument("interval", help="Monitoring interval in minutes")
        subparser.add_argument("--alert-email", help="Email for alerts")

    parser.add_subcommand("crawl", crawl_parser, "Crawl website recursively")
    parser.add_subcommand("extract", extract_parser, "Extract data from single page")
    parser.add_subcommand("monitor", monitor_parser, "Monitor website for changes")

    return parser


def demonstrate_usage():
    """Demonstrate different usage patterns."""

    print("🔧 Advanced Argument Parser - Usage Examples")
    print("=" * 55)

    # Example 1: File Processor
    print("\n📁 File Processor Tool:")
    print("-" * 25)
    processor = create_file_processor()

    # Simulate command line: file-processor input.txt --format json --compress --threads 4
    example_args = [
        "--input",
        "input.txt",
        "--format",
        "json",
        "--compress",
        "--threads",
        "4",
    ]
    try:
        args = processor.parse_args(example_args)
        print("✅ Parsed successfully!")
        print(f"  Input: {args.input}")
        print(f"  Format: {args.format}")
        print(f"  Compress: {args.compress}")
        print(f"  Threads: {args.threads}")
    except SystemExit:
        print("❌ Parsing failed")

    # Example 2: Data Analyzer
    print("\n📊 Data Analysis Tool:")
    print("-" * 25)
    analyzer = create_data_analyzer()

    example_args = [
        "--dataset",
        "data.csv",
        "--target",
        "price",
        "--method",
        "ml",
        "--parallel",
    ]
    try:
        args = analyzer.parse_args(example_args)
        print("✅ Parsed successfully!")
        print(f"  Dataset: {args.dataset}")
        print(f"  Target: {args.target}")
        print(f"  Method: {args.method}")
        print(f"  Parallel: {args.parallel}")
    except SystemExit:
        print("❌ Parsing failed")

    # Example 3: Web Scraper with subcommands
    print("\n🕷️  Web Scraper Tool:")
    print("-" * 22)
    scraper = create_web_scraper()

    example_args = ["--verbose", "crawl", "https://example.com", "2", "results.json"]
    try:
        args = scraper.parse_args(example_args)
        print("✅ Parsed successfully!")
        print(f"  Subcommand: {args.subcommand}")
        print(f"  URL: {args.url}")
        print(f"  Depth: {args.depth}")
        print(f"  Output: {args.output}")
        print(f"  Verbose: {args.verbose}")
    except SystemExit:
        print("❌ Parsing failed")


if __name__ == "__main__":
    demonstrate_usage()

    print("\n🎯 Key Benefits:")
    print("  ✅ Smart type inference - no need to specify types manually")
    print("  ✅ Auto-generated help text and validation")
    print("  ✅ Environment variable integration")
    print("  ✅ Config file support (JSON/YAML)")
    print("  ✅ Fuzzy argument matching with suggestions")
    print("  ✅ Subcommand support for complex tools")
    print("  ✅ Comprehensive error handling")
    print("  ✅ No more argparse boilerplate code")

    print("\n🚀 Ready to eliminate arg parsing headaches in your projects!")
