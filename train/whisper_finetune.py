"""
Fine-tune OpenAI Whisper for Bengali ASR.

This script fine-tunes Whisper (small/medium) on Bengali datasets.
Whisper is a transformer-based encoder-decoder model that performs
well on multilingual ASR.

Usage:
    python whisper_finetune.py \\
        --model_name openai/whisper-small \\
        --train_data ../data/processed/train.tsv \\
        --valid_data ../data/processed/valid.tsv \\
        --output_dir ../models/whisper_bengali

Author: BRAC Data Science Team  
Date: October 2025
"""

import argparse
from dataclasses import dataclass
from typing import Any, Dict, List, Union

import torch
from datasets import load_dataset, Audio
from transformers import (
    WhisperFeatureExtractor,
    WhisperTokenizer,
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    EarlyStoppingCallback
)
import evaluate
import numpy as np


@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    """
    Data collator for Whisper training.
    """
    
    processor: Any
    decoder_start_token_id: int
    
    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # Split inputs and labels
        input_features = [{"input_features": feature["input_features"]} for feature in features]
        label_features = [{"input_ids": feature["labels"]} for feature in features]
        
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")
        
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")
        
        # Replace padding with -100 to ignore in loss
        labels = labels_batch["input_ids"].masked_fill(
            labels_batch.attention_mask.ne(1), -100
        )
        
        # Cut off start token if present
        if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
            labels = labels[:, 1:]
        
        batch["labels"] = labels
        
        return batch


def prepare_dataset(batch, processor):
    """
    Prepare batch for Whisper training.
    """
    # Load and resample audio
    audio = batch["audio"]
    
    # Compute log-Mel spectrogram
    batch["input_features"] = processor.feature_extractor(
        audio["array"],
        sampling_rate=audio["sampling_rate"]
    ).input_features[0]
    
    # Tokenize transcript
    batch["labels"] = processor.tokenizer(batch["transcript"]).input_ids
    
    return batch


def compute_metrics(pred, processor, metric):
    """
    Compute WER metric for evaluation.
    """
    pred_ids = pred.predictions
    label_ids = pred.label_ids
    
    # Replace -100 with pad token
    label_ids[label_ids == -100] = processor.tokenizer.pad_token_id
    
    # Decode predictions and labels
    pred_str = processor.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = processor.tokenizer.batch_decode(label_ids, skip_special_tokens=True)
    
    # Compute WER
    wer_score = 100 * metric.compute(predictions=pred_str, references=label_str)
    
    return {"wer": wer_score}


def main():
    parser = argparse.ArgumentParser(
        description="Fine-tune Whisper for Bengali ASR"
    )
    parser.add_argument("--model_name", type=str, default="openai/whisper-small",
                       help="Whisper model variant (small, medium, large)")
    parser.add_argument("--train_data", type=str, required=True,
                       help="Path to training TSV")
    parser.add_argument("--valid_data", type=str, required=True,
                       help="Path to validation TSV")
    parser.add_argument("--output_dir", type=str, default="./whisper_bengali",
                       help="Output directory")
    parser.add_argument("--batch_size", type=int, default=16,
                       help="Training batch size")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=1,
                       help="Gradient accumulation steps")
    parser.add_argument("--learning_rate", type=float, default=1e-5,
                       help="Learning rate")
    parser.add_argument("--num_epochs", type=int, default=10,
                       help="Number of epochs")
    parser.add_argument("--warmup_steps", type=int, default=500,
                       help="Warmup steps")
    parser.add_argument("--early_stopping", action="store_true",
                       help="Enable early stopping")
    parser.add_argument("--early_stopping_patience", type=int, default=3,
                       help="Early stopping patience")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("Whisper Fine-tuning for Bengali ASR")
    print("="*60)
    print(f"Model: {args.model_name}")
    print(f"Train data: {args.train_data}")
    print(f"Valid data: {args.valid_data}")
    print(f"Output: {args.output_dir}")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.learning_rate}")
    print(f"Epochs: {args.num_epochs}")
    print("="*60 + "\n")
    
    # Load processor
    print("Loading processor...")
    feature_extractor = WhisperFeatureExtractor.from_pretrained(args.model_name)
    tokenizer = WhisperTokenizer.from_pretrained(
        args.model_name,
        language="Bengali",
        task="transcribe"
    )
    processor = WhisperProcessor.from_pretrained(
        args.model_name,
        language="Bengali",
        task="transcribe"
    )
    
    # Load datasets
    print("Loading datasets...")
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
    
    # Rename columns
    train_dataset = train_dataset.rename_column("path", "audio")
    valid_dataset = valid_dataset.rename_column("path", "audio")
    
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
    model = WhisperForConditionalGeneration.from_pretrained(args.model_name)
    
    # Set language and task tokens
    model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(
        language="bengali",
        task="transcribe"
    )
    model.config.suppress_tokens = []
    
    # Data collator
    data_collator = DataCollatorSpeechSeq2SeqWithPadding(
        processor=processor,
        decoder_start_token_id=model.config.decoder_start_token_id
    )
    
    # Load metric
    metric = evaluate.load("wer")
    
    # Training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        warmup_steps=args.warmup_steps,
        num_train_epochs=args.num_epochs,
        eval_strategy="steps",
        eval_steps=500,
        save_strategy="steps",
        save_steps=500,
        save_total_limit=3,
        logging_steps=100,
        fp16=True,
        gradient_checkpointing=True,
        load_best_model_at_end=True,
        metric_for_best_model="wer",
        greater_is_better=False,
        predict_with_generate=True,
        generation_max_length=225,
        report_to="none",
        push_to_hub=False
    )
    
    # Callbacks
    callbacks = []
    if args.early_stopping:
        callbacks.append(
            EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience)
        )
    
    # Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=data_collator,
        tokenizer=processor.feature_extractor,
        compute_metrics=lambda pred: compute_metrics(pred, processor, metric),
        callbacks=callbacks
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
