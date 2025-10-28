"""
Preprocess Bengali ASR datasets to uniform format.

This script:
1. Resamples audio to 16kHz
2. Normalizes audio (peak normalization)
3. Trims leading/trailing silence
4. Creates speaker-level train/valid/test splits (80/10/10)
5. Generates train.tsv, valid.tsv, test.tsv

Output format: path\ttranscript\tspeaker\tlocale

Usage:
    python preprocess.py \\
        --input_dirs ./raw/openslr_slr53 ./raw/common_voice_bn \\
        --output_dir ./processed \\
        --sample_rate 16000 \\
        --speaker_split

Author: BRAC Data Science Team
Date: October 2025
"""

import argparse
import csv
import json
import os
import warnings
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split

warnings.filterwarnings('ignore')


class AudioPreprocessor:
    """Handles audio preprocessing for Bengali ASR."""
    
    def __init__(self, target_sr: int = 16000, top_db: int = 30):
        """
        Initialize preprocessor.
        
        Args:
            target_sr: Target sampling rate (default: 16000 Hz)
            top_db: Threshold for silence trimming in dB (default: 30)
        """
        self.target_sr = target_sr
        self.top_db = top_db
    
    def process_audio(self, input_path: str, output_path: str) -> Dict:
        """
        Process a single audio file.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save processed audio
        
        Returns:
            Dict with processing stats (duration, original_sr, etc.)
        """
        try:
            # Load audio
            audio, sr = librosa.load(input_path, sr=None, mono=True)
            original_sr = sr
            original_duration = len(audio) / sr
            
            # Resample if needed
            if sr != self.target_sr:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=self.target_sr)
                sr = self.target_sr
            
            # Normalize (peak normalization)
            audio = self.normalize_audio(audio)
            
            # Trim silence
            audio = self.trim_silence(audio)
            
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save processed audio
            sf.write(output_path, audio, sr)
            
            return {
                "success": True,
                "duration": len(audio) / sr,
                "original_sr": original_sr,
                "original_duration": original_duration,
                "trimmed_seconds": original_duration - (len(audio) / sr)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def normalize_audio(self, audio: np.ndarray, target_level: float = 0.95) -> np.ndarray:
        """
        Normalize audio to target peak level.
        
        Args:
            audio: Audio signal
            target_level: Target peak level (0.0 to 1.0)
        
        Returns:
            Normalized audio
        """
        peak = np.abs(audio).max()
        if peak > 0:
            audio = audio * (target_level / peak)
        return audio
    
    def trim_silence(self, audio: np.ndarray) -> np.ndarray:
        """
        Trim leading and trailing silence.
        
        Args:
            audio: Audio signal
        
        Returns:
            Trimmed audio
        """
        trimmed, _ = librosa.effects.trim(audio, top_db=self.top_db)
        return trimmed


class DatasetSplitter:
    """Creates speaker-level train/valid/test splits."""
    
    def __init__(self, train_ratio: float = 0.8, valid_ratio: float = 0.1, 
                 test_ratio: float = 0.1, random_seed: int = 42):
        """
        Initialize splitter.
        
        Args:
            train_ratio: Fraction for training set
            valid_ratio: Fraction for validation set
            test_ratio: Fraction for test set
            random_seed: Random seed for reproducibility
        """
        assert abs(train_ratio + valid_ratio + test_ratio - 1.0) < 1e-6, \
            "Ratios must sum to 1.0"
        
        self.train_ratio = train_ratio
        self.valid_ratio = valid_ratio
        self.test_ratio = test_ratio
        self.random_seed = random_seed
    
    def split_by_speaker(self, data: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Split data by speaker to avoid data leakage.
        
        Args:
            data: List of dicts with keys: path, transcript, speaker, locale
        
        Returns:
            Tuple of (train_data, valid_data, test_data)
        """
        # Group by speaker
        speaker_to_samples = defaultdict(list)
        for sample in data:
            speaker = sample.get("speaker", "unknown")
            speaker_to_samples[speaker].append(sample)
        
        speakers = list(speaker_to_samples.keys())
        
        # First split: train vs (valid + test)
        train_speakers, temp_speakers = train_test_split(
            speakers,
            test_size=(self.valid_ratio + self.test_ratio),
            random_state=self.random_seed
        )
        
        # Second split: valid vs test
        valid_speakers, test_speakers = train_test_split(
            temp_speakers,
            test_size=self.test_ratio / (self.valid_ratio + self.test_ratio),
            random_state=self.random_seed
        )
        
        # Collect samples for each split
        train_data = []
        valid_data = []
        test_data = []
        
        for speaker in train_speakers:
            train_data.extend(speaker_to_samples[speaker])
        
        for speaker in valid_speakers:
            valid_data.extend(speaker_to_samples[speaker])
        
        for speaker in test_speakers:
            test_data.extend(speaker_to_samples[speaker])
        
        return train_data, valid_data, test_data


def load_openslr_data(data_dir: Path, processed_audio_dir: Path, 
                      preprocessor: AudioPreprocessor) -> List[Dict]:
    """
    Load and preprocess OpenSLR SLR53 dataset.
    
    Args:
        data_dir: Directory containing OpenSLR data
        processed_audio_dir: Directory to save processed audio
        preprocessor: AudioPreprocessor instance
    
    Returns:
        List of sample dicts
    """
    print(f"\nProcessing OpenSLR SLR53 from {data_dir}")
    samples = []
    
    # TODO: Adjust paths based on actual OpenSLR structure
    # This assumes a typical structure with train/valid/test subdirs
    for split_dir in ["train", "valid", "test"]:
        split_path = data_dir / split_dir
        if not split_path.exists():
            continue
        
        # Look for transcript file (usually .txt or .csv)
        transcript_file = split_path / "transcripts.txt"
        if not transcript_file.exists():
            print(f"  Warning: {transcript_file} not found, skipping...")
            continue
        
        with open(transcript_file, 'r', encoding='utf-8') as f:
            for line in tqdm(f, desc=f"  {split_dir}"):
                parts = line.strip().split('\t')
                if len(parts) < 2:
                    continue
                
                audio_id, transcript = parts[0], parts[1]
                audio_path = split_path / "audio" / f"{audio_id}.wav"
                
                if not audio_path.exists():
                    continue
                
                # Process audio
                output_path = processed_audio_dir / "openslr" / split_dir / f"{audio_id}.wav"
                result = preprocessor.process_audio(str(audio_path), str(output_path))
                
                if result["success"]:
                    samples.append({
                        "path": str(output_path),
                        "transcript": transcript.strip(),
                        "speaker": audio_id.split('_')[0],  # Extract speaker ID
                        "locale": "bn-BD"
                    })
    
    print(f"  Loaded {len(samples)} samples from OpenSLR")
    return samples


def load_common_voice_data(data_dir: Path, processed_audio_dir: Path,
                           preprocessor: AudioPreprocessor) -> List[Dict]:
    """
    Load and preprocess Mozilla Common Voice dataset.
    
    Args:
        data_dir: Directory containing Common Voice data
        processed_audio_dir: Directory to save processed audio
        preprocessor: AudioPreprocessor instance
    
    Returns:
        List of sample dicts
    """
    print(f"\nProcessing Common Voice from {data_dir}")
    samples = []
    
    try:
        from datasets import load_from_disk
        
        # Load cached dataset
        dataset = load_from_disk(str(data_dir))
        
        for split_name in ["train", "validation", "test"]:
            if split_name not in dataset:
                continue
            
            split_data = dataset[split_name]
            
            for i, sample in enumerate(tqdm(split_data, desc=f"  {split_name}")):
                audio_array = sample["audio"]["array"]
                sr = sample["audio"]["sampling_rate"]
                transcript = sample["sentence"]
                speaker_id = sample.get("client_id", f"speaker_{i}")
                
                # Save original audio temporarily
                temp_audio_path = processed_audio_dir / "temp" / f"cv_{i}.wav"
                temp_audio_path.parent.mkdir(parents=True, exist_ok=True)
                sf.write(str(temp_audio_path), audio_array, sr)
                
                # Process audio
                output_path = processed_audio_dir / "common_voice" / split_name / f"cv_{i}.wav"
                result = preprocessor.process_audio(str(temp_audio_path), str(output_path))
                
                # Clean up temp file
                temp_audio_path.unlink()
                
                if result["success"]:
                    samples.append({
                        "path": str(output_path),
                        "transcript": transcript.strip(),
                        "speaker": speaker_id,
                        "locale": "bn"
                    })
        
        print(f"  Loaded {len(samples)} samples from Common Voice")
        
    except Exception as e:
        print(f"  Error loading Common Voice: {str(e)}")
    
    return samples


def save_tsv(data: List[Dict], output_path: Path):
    """
    Save data to TSV file.
    
    Args:
        data: List of sample dicts
        output_path: Output TSV file path
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["path", "transcript", "speaker", "locale"])
        
        for sample in data:
            writer.writerow([
                sample["path"],
                sample["transcript"],
                sample["speaker"],
                sample["locale"]
            ])
    
    print(f"  Saved {len(data)} samples to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess Bengali ASR datasets"
    )
    parser.add_argument(
        "--input_dirs",
        nargs="+",
        required=True,
        help="Input directories containing raw datasets"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./processed",
        help="Output directory for processed data (default: ./processed)"
    )
    parser.add_argument(
        "--sample_rate",
        type=int,
        default=16000,
        help="Target sampling rate in Hz (default: 16000)"
    )
    parser.add_argument(
        "--speaker_split",
        action="store_true",
        help="Use speaker-level splits to avoid leakage"
    )
    parser.add_argument(
        "--top_db",
        type=int,
        default=30,
        help="Threshold for silence trimming in dB (default: 30)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("Bengali ASR Data Preprocessing")
    print("="*60)
    print(f"Input directories: {args.input_dirs}")
    print(f"Output directory: {args.output_dir}")
    print(f"Target sample rate: {args.sample_rate} Hz")
    print(f"Speaker-level split: {args.speaker_split}")
    print("="*60)
    
    output_dir = Path(args.output_dir)
    processed_audio_dir = output_dir / "audio"
    
    # Initialize preprocessor
    preprocessor = AudioPreprocessor(target_sr=args.sample_rate, top_db=args.top_db)
    
    # Load and process all datasets
    all_samples = []
    
    for input_dir in args.input_dirs:
        input_path = Path(input_dir)
        
        if "openslr" in str(input_path).lower():
            samples = load_openslr_data(input_path, processed_audio_dir, preprocessor)
            all_samples.extend(samples)
        
        elif "common_voice" in str(input_path).lower():
            samples = load_common_voice_data(input_path, processed_audio_dir, preprocessor)
            all_samples.extend(samples)
        
        # TODO: Add Bengali.AI loader
        # elif "bengaliai" in str(input_path).lower():
        #     samples = load_bengaliai_data(input_path, processed_audio_dir, preprocessor)
        #     all_samples.extend(samples)
    
    print(f"\nTotal samples loaded: {len(all_samples)}")
    
    # Split data
    if args.speaker_split:
        print("\nCreating speaker-level splits...")
        splitter = DatasetSplitter(train_ratio=0.8, valid_ratio=0.1, test_ratio=0.1)
        train_data, valid_data, test_data = splitter.split_by_speaker(all_samples)
    else:
        print("\nCreating random splits...")
        from sklearn.model_selection import train_test_split
        train_data, temp_data = train_test_split(all_samples, test_size=0.2, random_state=42)
        valid_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)
    
    print(f"  Train: {len(train_data)} samples")
    print(f"  Valid: {len(valid_data)} samples")
    print(f"  Test: {len(test_data)} samples")
    
    # Calculate duration statistics
    total_duration = sum([
        librosa.get_duration(path=sample["path"]) 
        for sample in train_data[:100]  # Sample for speed
    ]) * (len(train_data) / 100)
    
    print(f"\nEstimated total duration: {total_duration / 3600:.1f} hours")
    
    # Save splits
    print("\nSaving splits...")
    save_tsv(train_data, output_dir / "train.tsv")
    save_tsv(valid_data, output_dir / "valid.tsv")
    save_tsv(test_data, output_dir / "test.tsv")
    
    # Save statistics
    stats = {
        "total_samples": len(all_samples),
        "train_samples": len(train_data),
        "valid_samples": len(valid_data),
        "test_samples": len(test_data),
        "estimated_hours": total_duration / 3600,
        "target_sr": args.sample_rate,
        "speaker_split": args.speaker_split
    }
    
    stats_path = output_dir / "stats.json"
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n✓ Preprocessing complete!")
    print(f"  Output: {output_dir}")
    print(f"  Stats: {stats_path}")
    print("\nNext steps:")
    print("  1. Verify the TSV files")
    print("  2. Optionally run data augmentation: python augment.py")
    print("  3. Start training: cd ../train && python wav2vec2_finetune.py")


if __name__ == "__main__":
    main()
