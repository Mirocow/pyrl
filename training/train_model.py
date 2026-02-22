# FILE: training/train_model.py
"""
Pyrl Language Model Training Script
Fine-tunes a language model on Pyrl code examples

Usage:
    python train_model.py --config train_config.yaml
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path

try:
    import torch
    from transformers import (
        AutoTokenizer,
        AutoModelForCausalLM,
        TrainingArguments,
        Trainer,
        DataCollatorForLanguageModeling,
    )
    from datasets import Dataset
    from peft import LoraConfig, get_peft_model, TaskType
    HAS_ML = True
except ImportError:
    HAS_ML = False
    print("Warning: ML dependencies not installed. Install with: pip install torch transformers peft datasets")


def load_dataset(filepath: str) -> list:
    """Load training dataset from JSONL file"""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def prepare_dataset(data: list, tokenizer, max_length: int = 512):
    """Prepare dataset for training"""
    
    def format_example(example):
        """Format example for instruction tuning"""
        instruction = example.get('instruction', '')
        input_text = example.get('input', '')
        output = example.get('output', '')
        
        # Format as instruction-response
        if input_text:
            prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
        else:
            prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
        
        return prompt
    
    # Format all examples
    formatted_data = [format_example(ex) for ex in data]
    
    # Tokenize
    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            truncation=True,
            padding='max_length',
            max_length=max_length,
            return_tensors='pt'
        )
    
    # Create dataset
    dataset_dict = {'text': formatted_data}
    dataset = Dataset.from_dict(dataset_dict)
    
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=['text']
    )
    
    return tokenized_dataset


def train(config: dict):
    """Train the model"""
    
    if not HAS_ML:
        print("Error: ML dependencies required. Install with: pip install torch transformers peft datasets")
        return
    
    # Load dataset
    print(f"Loading dataset from {config['dataset_path']}...")
    data = load_dataset(config['dataset_path'])
    print(f"Loaded {len(data)} examples")
    
    # Load tokenizer and model
    print(f"Loading model: {config['model_name']}...")
    tokenizer = AutoTokenizer.from_pretrained(config['model_name'])
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        config['model_name'],
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    
    # Apply LoRA if configured
    if config.get('use_lora', True):
        print("Applying LoRA configuration...")
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=config.get('lora_r', 8),
            lora_alpha=config.get('lora_alpha', 32),
            lora_dropout=config.get('lora_dropout', 0.1),
            target_modules=config.get('lora_target_modules', ["q_proj", "v_proj"]),
        )
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
    
    # Prepare dataset
    print("Preparing dataset...")
    train_dataset = prepare_dataset(data, tokenizer, config.get('max_length', 512))
    
    # Split into train/val
    split = config.get('train_val_split', 0.9)
    split_idx = int(len(train_dataset) * split)
    train_data = train_dataset.select(range(split_idx))
    val_data = train_dataset.select(range(split_idx, len(train_dataset)))
    
    print(f"Train samples: {len(train_data)}, Val samples: {len(val_data)}")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.get('output_dir', './models/pyrl-model'),
        num_train_epochs=config.get('epochs', 3),
        per_device_train_batch_size=config.get('batch_size', 4),
        per_device_eval_batch_size=config.get('batch_size', 4),
        gradient_accumulation_steps=config.get('gradient_accumulation_steps', 4),
        learning_rate=config.get('learning_rate', 2e-4),
        weight_decay=config.get('weight_decay', 0.01),
        warmup_steps=config.get('warmup_steps', 100),
        eval_strategy="steps",
        eval_steps=config.get('eval_steps', 100),
        save_steps=config.get('save_steps', 100),
        save_total_limit=config.get('save_total_limit', 3),
        load_best_model_at_end=True,
        logging_dir=config.get('logging_dir', './logs'),
        logging_steps=10,
        fp16=torch.cuda.is_available(),
        report_to=config.get('report_to', 'tensorboard'),
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=val_data,
        data_collator=data_collator,
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save final model
    output_dir = config.get('output_dir', './models/pyrl-model')
    print(f"Saving model to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save training metadata
    metadata = {
        "model_name": config['model_name'],
        "dataset_size": len(data),
        "train_samples": len(train_data),
        "val_samples": len(val_data),
        "epochs": config.get('epochs', 3),
        "batch_size": config.get('batch_size', 4),
        "learning_rate": config.get('learning_rate', 2e-4),
        "trained_at": datetime.now().isoformat(),
        "pyrl_version": "2.0.0",
    }
    
    with open(os.path.join(output_dir, 'training_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("Training complete!")


def test_model(model_path: str, test_prompts: list):
    """Test the trained model"""
    
    if not HAS_ML:
        print("Error: ML dependencies required.")
        return
    
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    
    print("\n" + "="*60)
    print("Testing Pyrl Model")
    print("="*60)
    
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        print("-"*40)
        
        full_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"
        inputs = tokenizer(full_prompt, return_tensors="pt")
        
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract just the response part
        if "### Response:" in response:
            response = response.split("### Response:")[-1].strip()
        
        print(response)


def main():
    parser = argparse.ArgumentParser(description='Train Pyrl Language Model')
    parser.add_argument('--config', type=str, default='train_config.yaml', help='Path to config file')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--model_path', type=str, help='Path to model for testing')
    args = parser.parse_args()
    
    # Load config
    import yaml
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    if args.test:
        test_prompts = [
            "Create a function to calculate factorial",
            "Write a test for user authentication",
            "Generate a Vue component for a user card",
        ]
        model_path = args.model_path or config.get('output_dir', './models/pyrl-model')
        test_model(model_path, test_prompts)
    else:
        train(config)


if __name__ == "__main__":
    main()
