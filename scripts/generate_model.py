#!/usr/bin/env python3
"""
Generate Pyrl Language Model
Creates model files for the Pyrl language.
"""
import json
import os
import struct
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_config

# Get config
config = get_config()
MODEL_PATH = config.model_path


def generate_tokenizer():
    """Generate tokenizer files."""
    print("Generating tokenizer...")
    
    # Vocabulary - Pyrl specific tokens
    vocab = {
        # Special tokens
        "<pad>": 0,
        "<unk>": 1,
        "<bos>": 2,
        "<eos>": 3,
        "<mask>": 4,
        
        # Sigils
        "$": 5,
        "@": 6,
        "%": 7,
        "&": 8,
        
        # Operators
        "+": 10,
        "-": 11,
        "*": 12,
        "/": 13,
        "%": 14,
        "=": 15,
        "==": 16,
        "!=": 17,
        "<": 18,
        ">": 19,
        "<=": 20,
        ">=": 21,
        "**": 22,
        "//": 23,
        
        # Delimiters
        "(": 30,
        ")": 31,
        "[": 32,
        "]": 33,
        "{": 34,
        "}": 35,
        ",": 36,
        ":": 37,
        ".": 38,
        
        # Keywords
        "if": 100,
        "elif": 101,
        "else": 102,
        "while": 103,
        "for": 104,
        "in": 105,
        "def": 106,
        "return": 107,
        "break": 108,
        "continue": 109,
        "print": 110,
        "True": 111,
        "False": 112,
        "None": 113,
        "and": 114,
        "or": 115,
        "not": 116,
        "import": 117,
        "from": 118,
        "as": 119,
        "class": 120,
        "try": 121,
        "except": 122,
        "finally": 123,
        "raise": 124,
        "with": 125,
        "lambda": 126,
        "pass": 127,
    }
    
    # Add common identifiers and strings
    common_words = [
        "print", "len", "range", "str", "int", "float", "bool", "list", "dict",
        "name", "value", "result", "data", "item", "key", "index", "count",
        "self", "init", "main", "args", "kwargs",
        "hello", "world", "test", "example",
    ]
    
    idx = 200
    for word in common_words:
        if word not in vocab:
            vocab[word] = idx
            idx += 1
    
    # Add numbers 0-100
    for i in range(101):
        vocab[str(i)] = 1000 + i
    
    # Save vocab
    vocab_path = MODEL_PATH / "vocab.json"
    with open(vocab_path, "w") as f:
        json.dump(vocab, f, indent=2)
    print(f"  Saved vocab to {vocab_path} ({len(vocab)} tokens)")
    
    # Save merges file (placeholder for BPE)
    merges_path = MODEL_PATH / "merges.txt"
    with open(merges_path, "w") as f:
        f.write("#version: 0.1\n")
        for i in range(100):
            f.write(f"t {i}\n")
    print(f"  Saved merges to {merges_path}")
    
    return vocab


def generate_config():
    """Generate model configuration."""
    print("Generating config...")
    
    config = {
        "model_type": "pyrl-transformer",
        "architectures": ["PyrlForCausalLM"],
        "vocab_size": 32000,
        "hidden_size": 768,
        "intermediate_size": 3072,
        "num_hidden_layers": 12,
        "num_attention_heads": 12,
        "hidden_act": "gelu",
        "hidden_dropout_prob": 0.1,
        "attention_probs_dropout_prob": 0.1,
        "max_position_embeddings": 2048,
        "type_vocab_size": 2,
        "initializer_range": 0.02,
        "layer_norm_eps": 1e-12,
        "pad_token_id": 0,
        "bos_token_id": 2,
        "eos_token_id": 3,
        "torch_dtype": "float32",
        "transformers_version": "4.30.0",
    }
    
    config_path = MODEL_PATH / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"  Saved config to {config_path}")
    
    return config


def generate_model_weights(config):
    """Generate placeholder model weights."""
    print("Generating model weights...")
    
    import struct
    import random
    
    # Calculate approximate size
    hidden_size = config["hidden_size"]
    vocab_size = config["vocab_size"]
    num_layers = config["num_hidden_layers"]
    
    # Create a small placeholder file
    weights_path = MODEL_PATH / "pytorch_model.bin"
    
    # Generate deterministic random weights
    random.seed(42)
    
    with open(weights_path, "wb") as f:
        # Write header
        header = b"PYRL_MODEL_V1.0"
        f.write(header)
        
        # Write dimensions
        f.write(struct.pack("I", vocab_size))
        f.write(struct.pack("I", hidden_size))
        f.write(struct.pack("I", num_layers))
        
        # Write some placeholder weights (small file for demo)
        weight_count = 10000
        f.write(struct.pack("I", weight_count))
        
        for _ in range(weight_count):
            value = random.gauss(0, 0.02)
            f.write(struct.pack("f", value))
    
    file_size = weights_path.stat().st_size
    print(f"  Saved weights to {weights_path} ({file_size} bytes)")


def generate_tokenizer_config():
    """Generate tokenizer configuration."""
    print("Generating tokenizer config...")
    
    config = {
        "tokenizer_class": "PyrlTokenizer",
        "bos_token": "<bos>",
        "eos_token": "<eos>",
        "unk_token": "<unk>",
        "pad_token": "<pad>",
        "mask_token": "<mask>",
        "model_max_length": 2048,
        "do_lower_case": False,
    }
    
    config_path = MODEL_PATH / "tokenizer_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"  Saved tokenizer config to {config_path}")


def generate_special_tokens_map():
    """Generate special tokens map."""
    print("Generating special tokens map...")
    
    tokens_map = {
        "bos_token": "<bos>",
        "eos_token": "<eos>",
        "unk_token": "<unk>",
        "pad_token": "<pad>",
        "mask_token": "<mask>",
        "cls_token": "<cls>",
        "sep_token": "<sep>",
    }
    
    path = MODEL_PATH / "special_tokens_map.json"
    with open(path, "w") as f:
        json.dump(tokens_map, f, indent=2)
    print(f"  Saved special tokens map to {path}")


def main():
    """Main entry point."""
    print("=" * 50)
    print("Pyrl Model Generator")
    print("=" * 50)
    
    # Create model directory
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    print(f"Model path: {MODEL_PATH}")
    print()
    
    # Generate files
    vocab = generate_tokenizer()
    config = generate_config()
    generate_model_weights(config)
    generate_tokenizer_config()
    generate_special_tokens_map()
    
    print()
    print("=" * 50)
    print("Model generation complete!")
    print(f"Files generated in: {MODEL_PATH}")
    print("=" * 50)
    
    # List generated files
    print("\nGenerated files:")
    for f in MODEL_PATH.iterdir():
        size = f.stat().st_size
        print(f"  {f.name}: {size:,} bytes")


if __name__ == "__main__":
    main()
