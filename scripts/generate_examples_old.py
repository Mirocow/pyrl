#!/usr/bin/env python3
"""
Generate Pyrl Code Examples
Creates example files demonstrating Pyrl language features.
"""
import os
from pathlib import Path

# Get paths from environment or use defaults
EXAMPLES_DIR = Path(os.getenv("PYRL_EXAMPLES_DIR", "examples"))
MAX_EXAMPLES = int(os.getenv("PYRL_MAX_EXAMPLES", "100"))


# Example templates organized by category
EXAMPLE_TEMPLATES = {
    "variables": [
        "# Variable example {i}\n$name{i} = \"value{i}\"\n$age{i} = {age}\nprint($name{i} + \" is \" + str($age{i}))",
        "# Scalar variable\n$scalar{i} = {num}\nprint($scalar{i})",
        "# Array variable\n@array{i} = [{a}, {b}, {c}]\nprint(@array{i})",
        "# Hash variable\n%hash{i} = {{key1: \"{v1}\", key2: {num}}}\nprint(%hash{i})",
    ],
    "arithmetic": [
        "# Arithmetic {i}\n$a = {a}\n$b = {b}\n$sum = $a + $b\nprint($sum)",
        "# Multiplication\n$x{i} = {a} * {b}\nprint($x{i})",
        "# Division\n$div{i} = {a} / {b}\nprint($div{i})",
        "# Power\n$pow{i} = {a} ** {b}\nprint($pow{i})",
        "# Modulo\n$mod{i} = {a} % {b}\nprint($mod{i})",
    ],
    "control_flow": [
        "# If statement {i}\n$val = {num}\nif $val > 50:\n    print(\"greater\")\nelse:\n    print(\"smaller\")",
        "# While loop\n$i = 0\nwhile $i < {num}:\n    print($i)\n    $i = $i + 1",
        "# For loop\nfor $j in range({num}):\n    print($j)",
    ],
    "functions": [
        "# Function {i}\ndef add_{i}($a, $b):\n    return $a + $b\n$result = add_{i}({a}, {b})\nprint($result)",
        "# Recursive function\ndef countdown_{i}($n):\n    if $n <= 0:\n        return\n    print($n)\n    countdown_{i}($n - 1)\ncountdown_{i}({num})",
    ],
    "arrays": [
        "# Array operations {i}\n@arr{i} = [{a}, {b}, {c}, {d}]\nprint(len(@arr{i}))\nprint(@arr{i}[0])",
        "# Array iteration\n@items{i} = [\"a\", \"b\", \"c\"]\nfor $item in @items{i}:\n    print($item)",
    ],
    "hashes": [
        "# Hash operations {i}\n%data{i} = {{name: \"{name}\", value: {num}}}\nprint(%data{i}[\"name\"])",
    ],
}

NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]


def generate_example(i: int, category: str, template: str) -> str:
    """Generate a single example from a template."""
    import random
    random.seed(i * 100 + hash(category))

    # Generate values for placeholders
    values = {
        "i": i,
        "num": random.randint(1, 100),
        "age": random.randint(18, 80),
        "a": random.randint(1, 50),
        "b": random.randint(1, 20),
        "c": random.randint(1, 30),
        "d": random.randint(1, 40),
        "v1": random.choice(NAMES),
        "name": random.choice(NAMES),
    }

    return template.format(**values)


def generate_examples_file(filename: str, count: int, categories: list):
    """Generate a file with multiple examples."""
    filepath = EXAMPLES_DIR / filename
    examples = []

    for i in range(count):
        category = categories[i % len(categories)]
        template = EXAMPLE_TEMPLATES[category][i % len(EXAMPLE_TEMPLATES[category])]
        example = generate_example(i, category, template)
        examples.append(example)

    with open(filepath, "w") as f:
        f.write(f"# Auto-generated Pyrl Examples\n")
        f.write(f"# Count: {count}\n\n")
        f.write("\n\n".join(examples))

    print(f"Generated {filepath}: {count} examples")
    return filepath


def generate_all_examples():
    """Generate all example files."""
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating Pyrl examples...")
    print(f"Output directory: {EXAMPLES_DIR}")
    print()

    # Generate by category
    categories = list(EXAMPLE_TEMPLATES.keys())
    examples_per_category = MAX_EXAMPLES // len(categories)

    generated_files = []

    for category in categories:
        filename = f"generated_{category}.pyrl"
        filepath = generate_examples_file(
            filename,
            examples_per_category,
            [category]
        )
        generated_files.append(filepath)

    # Generate mixed examples
    total_mixed = MAX_EXAMPLES - (examples_per_category * len(categories))
    if total_mixed > 0:
        filepath = generate_examples_file(
            "generated_mixed.pyrl",
            total_mixed,
            categories
        )
        generated_files.append(filepath)

    # Generate single combined file
    all_examples = []
    for category in categories:
        for i, template in enumerate(EXAMPLE_TEMPLATES[category]):
            all_examples.append(generate_example(i, category, template))

    combined_path = EXAMPLES_DIR / "generated_all.pyrl"
    with open(combined_path, "w") as f:
        f.write(f"# All Generated Pyrl Examples\n")
        f.write(f"# Total: {len(all_examples)}\n\n")
        f.write("\n\n".join(all_examples))

    print(f"Generated {combined_path}: {len(all_examples)} examples")

    return generated_files


def main():
    """Main entry point."""
    print("=" * 50)
    print("Pyrl Example Generator")
    print("=" * 50)
    print()

    files = generate_all_examples()

    print()
    print("=" * 50)
    print("Example generation complete!")
    print(f"Total files: {len(files) + 1}")
    print("=" * 50)


if __name__ == "__main__":
    main()
