"""
Evaluate Bengali ASR models and produce WER/CER reports.

This script:
1. Loads trained model checkpoint
2. Evaluates on test set
3. Produces detailed WER/CER reports
4. Analyzes common error patterns (numbers, names, code-switching)

Usage:
    python eval_wer_cer.py \\
        --model_path ../models/wav2vec2_brac_dialect/checkpoint-best \\
        --test_data ../data/processed/test.tsv \\
        --output_dir ./results \\
        --detailed_analysis

Author: BRAC Data Science Team
Date: October 2025
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple

import pandas as pd
import torch
from datasets import load_dataset, Audio
from transformers import (
    Wav2Vec2Processor,
    Wav2Vec2ForCTC,
    WhisperProcessor,
    WhisperForConditionalGeneration
)
from jiwer import wer, cer
from tqdm import tqdm


class ASREvaluator:
    """Evaluate ASR models on test data."""
    
    def __init__(self, model_path: str, model_type: str = "wav2vec2"):
        """
        Initialize evaluator.
        
        Args:
            model_path: Path to model checkpoint
            model_type: "wav2vec2" or "whisper"
        """
        self.model_path = model_path
        self.model_type = model_type
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading {model_type} model from {model_path}...")
        print(f"Using device: {self.device}")
        
        if model_type == "wav2vec2":
            self.processor = Wav2Vec2Processor.from_pretrained(model_path)
            self.model = Wav2Vec2ForCTC.from_pretrained(model_path).to(self.device)
        elif model_type == "whisper":
            self.processor = WhisperProcessor.from_pretrained(model_path)
            self.model = WhisperForConditionalGeneration.from_pretrained(model_path).to(self.device)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        self.model.eval()
    
    def transcribe_wav2vec2(self, audio_path: str) -> str:
        """Transcribe audio using Wav2Vec2."""
        import librosa
        
        # Load audio
        audio, sr = librosa.load(audio_path, sr=16000)
        
        # Process
        inputs = self.processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            logits = self.model(inputs.input_values.to(self.device)).logits
        
        # Decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        
        return transcription
    
    def transcribe_whisper(self, audio_path: str) -> str:
        """Transcribe audio using Whisper."""
        import librosa
        
        # Load audio
        audio, sr = librosa.load(audio_path, sr=16000)
        
        # Process
        input_features = self.processor(
            audio,
            sampling_rate=16000,
            return_tensors="pt"
        ).input_features.to(self.device)
        
        # Generate
        with torch.no_grad():
            predicted_ids = self.model.generate(input_features)
        
        # Decode
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        return transcription
    
    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio (auto-select method based on model type)."""
        if self.model_type == "wav2vec2":
            return self.transcribe_wav2vec2(audio_path)
        else:
            return self.transcribe_whisper(audio_path)
    
    def evaluate_dataset(self, test_tsv: str) -> Tuple[List[str], List[str], List[str]]:
        """
        Evaluate model on test dataset.
        
        Args:
            test_tsv: Path to test TSV file
        
        Returns:
            Tuple of (predictions, references, audio_paths)
        """
        # Load test data
        df = pd.read_csv(test_tsv, sep='\t')
        
        predictions = []
        references = []
        audio_paths = []
        
        print(f"\nEvaluating on {len(df)} samples...")
        
        for _, row in tqdm(df.iterrows(), total=len(df)):
            audio_path = row['path']
            reference = row['transcript']
            
            try:
                prediction = self.transcribe(audio_path)
                
                predictions.append(prediction)
                references.append(reference)
                audio_paths.append(audio_path)
                
            except Exception as e:
                print(f"Error processing {audio_path}: {str(e)}")
                continue
        
        return predictions, references, audio_paths


def analyze_errors(predictions: List[str], references: List[str]) -> Dict:
    """
    Analyze common error patterns.
    
    Args:
        predictions: List of predicted transcripts
        references: List of reference transcripts
    
    Returns:
        Dictionary with error analysis
    """
    import difflib
    
    analysis = {
        "total_samples": len(predictions),
        "substitutions": [],
        "deletions": [],
        "insertions": [],
        "numbers_errors": 0,
        "code_switching_errors": 0
    }
    
    # Check for Bengali number words
    number_words = ['শূন্য', 'এক', 'দুই', 'তিন', 'চার', 'পাঁচ', 'ছয়', 'সাত', 'আট', 'নয়']
    
    # Check for English words (code-switching)
    english_pattern = re.compile(r'[a-zA-Z]+')
    
    for pred, ref in zip(predictions, references):
        # Count number-related errors
        for num_word in number_words:
            if num_word in ref and num_word not in pred:
                analysis["numbers_errors"] += 1
                break
        
        # Count code-switching errors
        ref_has_english = bool(english_pattern.search(ref))
        pred_has_english = bool(english_pattern.search(pred))
        if ref_has_english != pred_has_english:
            analysis["code_switching_errors"] += 1
        
        # Word-level diff
        ref_words = ref.split()
        pred_words = pred.split()
        
        matcher = difflib.SequenceMatcher(None, ref_words, pred_words)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    if i < len(ref_words) and j < len(pred_words):
                        analysis["substitutions"].append((ref_words[i], pred_words[j]))
            elif tag == 'delete':
                for i in range(i1, i2):
                    if i < len(ref_words):
                        analysis["deletions"].append(ref_words[i])
            elif tag == 'insert':
                for j in range(j1, j2):
                    if j < len(pred_words):
                        analysis["insertions"].append(pred_words[j])
    
    # Count most common errors
    analysis["most_common_substitutions"] = Counter(analysis["substitutions"]).most_common(20)
    analysis["most_common_deletions"] = Counter(analysis["deletions"]).most_common(20)
    analysis["most_common_insertions"] = Counter(analysis["insertions"]).most_common(20)
    
    # Remove full lists to reduce output size
    del analysis["substitutions"]
    del analysis["deletions"]
    del analysis["insertions"]
    
    return analysis


import re


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate Bengali ASR model"
    )
    parser.add_argument("--model_path", type=str, required=True,
                       help="Path to model checkpoint")
    parser.add_argument("--model_type", type=str, default="wav2vec2",
                       choices=["wav2vec2", "whisper"],
                       help="Model type")
    parser.add_argument("--test_data", type=str, required=True,
                       help="Path to test TSV")
    parser.add_argument("--output_dir", type=str, default="./results",
                       help="Output directory for results")
    parser.add_argument("--detailed_analysis", action="store_true",
                       help="Perform detailed error analysis")
    parser.add_argument("--save_predictions", action="store_true",
                       help="Save predictions to file")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("Bengali ASR Model Evaluation")
    print("="*60)
    print(f"Model: {args.model_path}")
    print(f"Model type: {args.model_type}")
    print(f"Test data: {args.test_data}")
    print(f"Output: {args.output_dir}")
    print("="*60 + "\n")
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize evaluator
    evaluator = ASREvaluator(args.model_path, args.model_type)
    
    # Evaluate
    predictions, references, audio_paths = evaluator.evaluate_dataset(args.test_data)
    
    # Calculate metrics
    print("\n" + "="*60)
    print("Results")
    print("="*60)
    
    wer_score = wer(references, predictions)
    cer_score = cer(references, predictions)
    
    print(f"Word Error Rate (WER): {wer_score*100:.2f}%")
    print(f"Character Error Rate (CER): {cer_score*100:.2f}%")
    print(f"Total samples: {len(predictions)}")
    
    # Save metrics
    metrics = {
        "model_path": args.model_path,
        "model_type": args.model_type,
        "test_data": args.test_data,
        "wer": wer_score,
        "cer": cer_score,
        "num_samples": len(predictions)
    }
    
    # Detailed analysis
    if args.detailed_analysis:
        print("\nPerforming detailed error analysis...")
        error_analysis = analyze_errors(predictions, references)
        metrics["error_analysis"] = error_analysis
        
        print(f"\nError Analysis:")
        print(f"  Numbers errors: {error_analysis['numbers_errors']}")
        print(f"  Code-switching errors: {error_analysis['code_switching_errors']}")
        print(f"\nMost common substitutions:")
        for (ref_word, pred_word), count in error_analysis['most_common_substitutions'][:10]:
            print(f"  {ref_word} → {pred_word}: {count}")
    
    # Save metrics
    metrics_file = output_dir / "metrics.json"
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Metrics saved to {metrics_file}")
    
    # Save predictions
    if args.save_predictions:
        predictions_file = output_dir / "predictions.tsv"
        results_df = pd.DataFrame({
            'audio_path': audio_paths,
            'reference': references,
            'prediction': predictions
        })
        results_df.to_csv(predictions_file, sep='\t', index=False)
        print(f"✓ Predictions saved to {predictions_file}")
    
    print("\n✓ Evaluation complete!")


if __name__ == "__main__":
    main()
