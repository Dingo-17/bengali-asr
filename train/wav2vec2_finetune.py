"""
Fine-tune Wav2Vec2-XLSR-53 for Bengali ASR using Hugging Face Transformers.

This script fine-tunes facebook/wav2vec2-large-xlsr-53 on Bengali datasets
with CTC loss for automatic speech recognition.

Features:
- Mixed precision training (FP16)
- Gradient accumulation
- Checkpointing
- W&B logging (optional)
- Early stopping

Usage:
    python wav2vec2_finetune.py \\
        --config finetune_config.yaml \\
        --model_name facebook/wav2vec2-large-xlsr-53 \\
        --output_dir ../models/wav2vec2_bengali \\
        --train_data ../data/processed/train.tsv \\
        --valid_data ../data/processed/valid.tsv

Author: BRAC Data Science Team
Date: October 2025
"""

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

import torch
import torchaudio
from torch.utils.data import Dataset
from transformers import (
    Wav2Vec2CTCTokenizer,
    Wav2Vec2FeatureExtractor,
    Wav2Vec2Processor,
    Wav2Vec2ForCTC,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from datasets import load_dataset, Audio
import pandas as pd
import numpy as np

# Optional W&B integration
try:
    import wandb
    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False


@dataclass
class DataCollatorCTCWithPadding:
    """
    Data collator that will dynamically pad the inputs received.
    
    Args:
        processor: Wav2Vec2Processor
        padding: Whether to pad to longest or max_length
    """
    
    processor: Wav2Vec2Processor
    padding: Union[bool, str] = True
    
    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # Split inputs and labels
        input_features = [{"input_values": feature["input_values"]} for feature in features]
        label_features = [{"input_ids": feature["labels"]} for feature in features]
        
        batch = self.processor.pad(
            input_features,
            padding=self.padding,
            return_tensors="pt",
        )
        
        labels_batch = self.processor.pad(
            labels=label_features,
            padding=self.padding,
            return_tensors="pt",
        )
        
        # Replace padding with -100 to ignore in loss
        labels = labels_batch["input_ids"].masked_fill(
            labels_batch.attention_mask.ne(1), -100
        )
        
        batch["labels"] = labels
        
        return batch


def load_vocab_from_dataset(train_tsv: str, valid_tsv: str) -> Dict[str, int]:
    """
    Extract vocabulary from training data.
    
    Args:
        train_tsv: Path to training TSV
        valid_tsv: Path to validation TSV
    
    Returns:
        Dictionary mapping characters to IDs
    """
    print("Extracting vocabulary from dataset...")
    
    train_df = pd.read_csv(train_tsv, sep='\t')
    valid_df = pd.read_csv(valid_tsv, sep='\t')
    
    # Combine all transcripts
    all_text = ' '.join(train_df['transcript'].tolist() + valid_df['transcript'].tolist())
    
    # Extract unique characters
    vocab_set = set(all_text)
    
    # Create vocab dict
    vocab_dict = {char: idx for idx, char in enumerate(sorted(vocab_set))}
    
    # Add special tokens
    vocab_dict['[UNK]'] = len(vocab_dict)
    vocab_dict['[PAD]'] = len(vocab_dict)
    
    print(f"Vocabulary size: {len(vocab_dict)}")
    print(f"Sample characters: {list(vocab_dict.keys())[:10]}")
    
    return vocab_dict


def create_processor(vocab_dict: Dict[str, int], model_name: str) -> Wav2Vec2Processor:
    """
    Create Wav2Vec2 processor with custom vocabulary.
    
    Args:
        vocab_dict: Character to ID mapping
        model_name: Pretrained model name
    
    Returns:
        Wav2Vec2Processor
    """
    # Save vocab as JSON
    vocab_path = Path("./vocab.json")
    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(vocab_dict, f, ensure_ascii=False, indent=2)
    
    # Create tokenizer
    tokenizer = Wav2Vec2CTCTokenizer(
        str(vocab_path),
        unk_token="[UNK]",
        pad_token="[PAD]",
        word_delimiter_token="|"
    )
    
    # Create feature extractor
    feature_extractor = Wav2Vec2FeatureExtractor(
        feature_size=1,
        sampling_rate=16000,
        padding_value=0.0,
        do_normalize=True,
        return_attention_mask=True
    )
    
    # Combine into processor
    processor = Wav2Vec2Processor(
        feature_extractor=feature_extractor,
        tokenizer=tokenizer
    )
    
    return processor


def prepare_dataset(batch, processor):
    """
    Prepare a single batch for training.
    
    Args:
        batch: Dictionary with 'audio' and 'transcript' keys
        processor: Wav2Vec2Processor
    
    Returns:
        Batch with processed features
    """
    # Process audio
    audio = batch["audio"]["array"]
    batch["input_values"] = processor(
        audio,
        sampling_rate=16000,
        return_tensors="pt"
    ).input_values[0]
    
    # Process text
    with processor.as_target_processor():
        batch["labels"] = processor(batch["transcript"]).input_ids
    
    return batch


def compute_metrics(pred, processor):
    """
    Compute WER (Word Error Rate) metric.
    
    Args:
        pred: Predictions from model
        processor: Wav2Vec2Processor
    
    Returns:
        Dictionary with WER metric
    """
    from jiwer import wer
    
    pred_logits = pred.predictions
    pred_ids = np.argmax(pred_logits, axis=-1)
    
    pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id
    
    pred_str = processor.batch_decode(pred_ids)
    label_str = processor.batch_decode(pred.label_ids, group_tokens=False)
    
    wer_score = wer(label_str, pred_str)
    
    return {"wer": wer_score}


def main():
    parser = argparse.ArgumentParser(
        description="Fine-tune Wav2Vec2 for Bengali ASR"
    )
    parser.add_argument("--model_name", type=str, default="facebook/wav2vec2-large-xlsr-53",
                       help="Pretrained model name or path")
    parser.add_argument("--train_data", type=str, required=True,
                       help="Path to training TSV")
    parser.add_argument("--valid_data", type=str, required=True,
                       help="Path to validation TSV")
    parser.add_argument("--output_dir", type=str, default="./wav2vec2_bengali",
                       help="Output directory for model")
    parser.add_argument("--batch_size", type=int, default=8,
                       help="Training batch size")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=2,
                       help="Gradient accumulation steps")
    parser.add_argument("--learning_rate", type=float, default=3e-4,
                       help="Learning rate")
    parser.add_argument("--num_epochs", type=int, default=30,
                       help="Number of training epochs")
    parser.add_argument("--warmup_steps", type=int, default=500,
                       help="Warmup steps")
    parser.add_argument("--mixed_precision", action="store_true",
                       help="Use FP16 mixed precision")
    parser.add_argument("--wandb_logging", action="store_true",
                       help="Enable W&B logging")
    parser.add_argument("--early_stopping_patience", type=int, default=5,
                       help="Early stopping patience")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("Wav2Vec2 Fine-tuning for Bengali ASR")
    print("="*60)
    print(f"Model: {args.model_name}")
    print(f"Train data: {args.train_data}")
    print(f"Valid data: {args.valid_data}")
    print(f"Output: {args.output_dir}")
    print(f"Batch size: {args.batch_size} (grad_accum: {args.gradient_accumulation_steps})")
    print(f"Learning rate: {args.learning_rate}")
    print(f"Epochs: {args.num_epochs}")
    print(f"Mixed precision: {args.mixed_precision}")
    print("="*60 + "\n")
    
    # Initialize W&B if requested
    if args.wandb_logging and WANDB_AVAILABLE:
        wandb.init(project="bengali-asr-wav2vec2", config=vars(args))
    
    # Create vocabulary
    vocab_dict = load_vocab_from_dataset(args.train_data, args.valid_data)
    
    # Create processor
    processor = create_processor(vocab_dict, args.model_name)
    
    # Load datasets
    print("\nLoading datasets...")
    train_dataset = load_dataset(
        'csv',
        data_files={'train': args.train_data},
        delimiter='\t'
    )['train']
    
    valid_dataset = load_dataset(
        'csv',
        data_files={'validation': args.valid_data},
        delimiter='\t'
    )['validation']
    
    # Cast audio column
    train_dataset = train_dataset.cast_column("path", Audio(sampling_rate=16000))
    valid_dataset = valid_dataset.cast_column("path", Audio(sampling_rate=16000))
    
    # Rename 'path' to 'audio' for easier processing
    train_dataset = train_dataset.rename_column("path", "audio")
    valid_dataset = valid_dataset.rename_column("audio", "audio")
    
    # Prepare datasets
    print("Preparing datasets...")
    train_dataset = train_dataset.map(
        lambda batch: prepare_dataset(batch, processor),
        remove_columns=train_dataset.column_names,
        num_proc=4
    )
    
    valid_dataset = valid_dataset.map(
        lambda batch: prepare_dataset(batch, processor),
        remove_columns=valid_dataset.column_names,
        num_proc=4
    )
    
    # Load model
    print(f"\nLoading model: {args.model_name}")
    model = Wav2Vec2ForCTC.from_pretrained(
        args.model_name,
        attention_dropout=0.1,
        hidden_dropout=0.1,
        feat_proj_dropout=0.0,
        mask_time_prob=0.05,
        layerdrop=0.1,
        ctc_loss_reduction="mean",
        pad_token_id=processor.tokenizer.pad_token_id,
        vocab_size=len(processor.tokenizer)
    )
    
    # Freeze feature extractor
    model.freeze_feature_encoder()
    
    # Data collator
    data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        group_by_length=True,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        eval_strategy="steps",
        eval_steps=500,
        save_steps=500,
        save_total_limit=3,
        logging_steps=100,
        learning_rate=args.learning_rate,
        warmup_steps=args.warmup_steps,
        num_train_epochs=args.num_epochs,
        fp16=args.mixed_precision,
        gradient_checkpointing=True,
        load_best_model_at_end=True,
        metric_for_best_model="wer",
        greater_is_better=False,
        push_to_hub=False,
        report_to="wandb" if (args.wandb_logging and WANDB_AVAILABLE) else "none"
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=data_collator,
        tokenizer=processor.feature_extractor,
        compute_metrics=lambda pred: compute_metrics(pred, processor),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience)]
    )
    
    # Train
    print("\n" + "="*60)
    print("Starting training...")
    print("="*60 + "\n")
    
    trainer.train()
    
    # Save final model
    print("\nSaving final model...")
    trainer.save_model(args.output_dir)
    processor.save_pretrained(args.output_dir)
    
    # Evaluate
    print("\nEvaluating on validation set...")
    metrics = trainer.evaluate()
    print(f"Validation WER: {metrics['eval_wer']:.4f}")
    
    print("\n✓ Training complete!")
    print(f"  Model saved to: {args.output_dir}")
    print(f"  Final WER: {metrics['eval_wer']:.4f}")


if __name__ == "__main__":
    main()
