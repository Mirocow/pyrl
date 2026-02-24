# Pyrl AI Model

Pretrained language model for Pyrl code generation and completion.

## Overview

Pyrl includes a pretrained transformer-based model capable of:

- **Code completion** — Complete partially written code
- **Code generation** — Generate code from descriptions
- **Syntax learning** — Understand Pyrl grammar patterns

## Model Specifications

| Property | Value |
|----------|-------|
| **Architecture** | Transformer Encoder-Decoder |
| **Tokenizer** | Byte Pair Encoding (BPE) |
| **Vocabulary Size** | 10,000 tokens |
| **Model Size** | ~50MB |
| **Training Data** | 10,000+ Pyrl examples |

## Model Files

```
models/pyrl-model/
├── config.json              # Model configuration
├── vocab.json               # BPE vocabulary
├── tokenizer_config.json    # Tokenizer settings
├── special_tokens_map.json  # Special tokens
└── training_stats.json      # Training statistics
```

## Using the Model

### Python API

```python
from scripts.model_inference import PyrlModel

# Load model
model = PyrlModel.load("models/pyrl-model")

# Generate code
prompt = "def fibonacci($n):"
code = model.generate(prompt, max_length=100)
print(code)
```

### Command Line

```bash
# Interactive generation
python scripts/model_inference.py --interactive

# Generate from prompt
python scripts/model_inference.py --prompt "def factorial($n):"

# Batch generation
python scripts/model_inference.py --file prompts.txt --output generated.pyrl
```

## Training Your Own Model

### Data Preparation

```bash
# Generate training examples
python scripts/generate_examples.py --count 10000 --output training_data/

# The generator creates:
# - Variable declarations
# - Function definitions
# - Class definitions
# - Control flow patterns
# - Regular expressions
# - Web handlers
```

### Training

```bash
# Basic training
python scripts/train_model.py --data training_data/ --epochs 10

# Advanced options
python scripts/train_model.py \
    --data training_data/ \
    --epochs 50 \
    --batch-size 32 \
    --learning-rate 0.0001 \
    --output models/my-model/
```

### Training Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--epochs` | 10 | Number of training epochs |
| `--batch-size` | 16 | Batch size |
| `--learning-rate` | 0.0001 | Learning rate |
| `--warmup-steps` | 1000 | Warmup steps |
| `--max-length` | 512 | Maximum sequence length |
| `--output` | models/pyrl-model | Output directory |

## Grammar Feature Extraction

The model uses grammar-aware feature extraction for better understanding:

```python
from scripts.train_model import GrammarFeatureExtractor

extractor = GrammarFeatureExtractor()

# Extract features from code
features = extractor.extract_features("""
def greet($name):
    return "Hello, " + $name
""")

# Features include:
# - Parse tree depth
# - Node type counts
# - Variable sigil distribution
# - Control flow complexity
```

## Docker Training

For GPU-accelerated training:

```bash
# Build training image
docker build -f docker/Dockerfile.training -t pyrl-training .

# Run training with GPU
docker run --gpus all \
    -v $(pwd)/models:/app/output \
    -v $(pwd)/examples:/app/examples \
    pyrl-training \
    python scripts/train_model.py --epochs 50
```

## Model Inference Server

Deploy the model as a REST API:

```bash
# Start inference server
docker-compose --profile inference up -d model-inference

# Or manually
python -m uvicorn docker.api_server:app --host 0.0.0.0 --port 8001
```

### API Endpoints

**POST /generate**
```json
{
    "prompt": "def sort_array(@arr):",
    "max_length": 100,
    "temperature": 0.7
}
```

Response:
```json
{
    "generated": "def sort_array(@arr):\n    @result = []\n    for $item in sorted(@arr):\n        @result.append($item)\n    return @result"
}
```

**POST /complete**
```json
{
    "code": "def factorial($n):\n    if $n <= 1:",
    "cursor_position": 30
}
```

## Performance

| Metric | Value |
|--------|-------|
| **Parse Success Rate** | 85%+ |
| **Code Validity** | 90%+ |
| **Inference Time** | <100ms |

## Limitations

- Model trained on synthetic data
- May generate syntactically correct but semantically incorrect code
- Limited understanding of complex control flow
- Best suited for code completion, not generation from scratch

## Future Improvements

- [ ] Fine-tuning on real-world Pyrl projects
- [ ] Larger model size options
- [ ] Multi-language support (generate Pyrl from Python)
- [ ] Code explanation capabilities
- [ ] Bug detection and fixing

## License

MIT License
