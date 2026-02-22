# Pyrl Language Model

## Model Information

- **Base Model**: GPT-2 (or any compatible causal LM)
- **Training Method**: Supervised Fine-Tuning (SFT) with LoRA
- **Dataset Size**: 32 examples (expandable)
- **Languages**: Pyrl code generation

## Model Files

```
models/pyrl-model/
├── config.json           # Model configuration
├── pytorch_model.bin     # Model weights
├── tokenizer.json        # Tokenizer
├── tokenizer_config.json # Tokenizer config
├── training_metadata.json # Training info
└── special_tokens_map.json
```

## Training Metadata

```json
{
    "model_name": "gpt2",
    "dataset_size": 32,
    "epochs": 3,
    "batch_size": 4,
    "learning_rate": 2e-4,
    "pyrl_version": "2.0.0"
}
```

## Usage

### Python

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model
tokenizer = AutoTokenizer.from_pretrained("./models/pyrl-model")
model = AutoModelForCausalLM.from_pretrained("./models/pyrl-model")

# Generate
prompt = "### Instruction:\nCreate a function to sort an array\n\n### Response:\n"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0]))
```

### Via PyrlAI

```python
from pyrl_ai import PyrlAI

ai = PyrlAI()
ai.set_llm_client(model)  # Pass your LLM client
result = ai.generate_code("Create a factorial function")
```

## Model Capabilities

The model is trained to:

1. **Generate valid Pyrl code** from natural language descriptions
2. **Understand Pyrl syntax** including sigils, operators, and control structures
3. **Suggest appropriate plugins** for advanced functionality
4. **Explain generated code** in natural language

## Example Prompts

| Prompt | Expected Output |
|--------|-----------------|
| "Create a function to add two numbers" | `&add($a, $b) = { return $a + $b }` |
| "Generate a Vue component for a user" | `vue "UserCard" { ... }` |
| "Write a test for string operations" | `test "String Tests" { ... }` |
| "Create a hash for user data" | `%user = {"name": "", "email": ""}` |

## Extending the Model

### Adding Training Data

1. Edit `training/dataset.jsonl`
2. Add new examples following the format:
   ```json
   {
       "instruction": "Description",
       "input": "Optional context",
       "output": "Pyrl code",
       "category": "category",
       "difficulty": "easy|medium|hard"
   }
   ```
3. Re-run training: `python training/train_model.py`

### Fine-tuning Parameters

Edit `training/train_config.yaml`:

```yaml
epochs: 3              # More epochs for larger datasets
batch_size: 4          # Adjust based on GPU memory
learning_rate: 2e-4    # Lower for stability
lora_r: 8              # LoRA rank (higher = more parameters)
```
