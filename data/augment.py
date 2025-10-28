"""
Data augmentation utilities for Bengali ASR.

Provides functions for:
1. Speed perturbation (0.9x, 1.0x, 1.1x)
2. Noise addition (background noise, white noise)
3. Volume augmentation

Usage:
    python augment.py \\
        --input data/processed/train.tsv \\
        --output data/augmented/train_augmented.tsv \\
        --speed_perturbation \\
        --noise_injection

Author: BRAC Data Science Team
Date: October 2025
"""

import argparse
import csv
import random
from pathlib import Path
from typing import List, Tuple

import librosa
import numpy as np
import soundfile as sf
from tqdm import tqdm


class AudioAugmenter:
    """Audio augmentation for speech data."""
    
    def __init__(self, sr: int = 16000, seed: int = 42):
        """
        Initialize augmenter.
        
        Args:
            sr: Sampling rate
            seed: Random seed for reproducibility
        """
        self.sr = sr
        self.rng = random.Random(seed)
        np.random.seed(seed)
    
    def speed_perturbation(self, audio: np.ndarray, speed_factor: float) -> np.ndarray:
        """
        Change audio speed without changing pitch.
        
        Args:
            audio: Input audio signal
            speed_factor: Speed multiplier (e.g., 0.9 = slower, 1.1 = faster)
        
        Returns:
            Speed-perturbed audio
        """
        return librosa.effects.time_stretch(audio, rate=speed_factor)
    
    def add_white_noise(self, audio: np.ndarray, noise_level: float = 0.005) -> np.ndarray:
        """
        Add white noise to audio.
        
        Args:
            audio: Input audio signal
            noise_level: Standard deviation of noise (default: 0.005)
        
        Returns:
            Audio with added noise
        """
        noise = np.random.normal(0, noise_level, audio.shape)
        augmented = audio + noise
        # Normalize to prevent clipping
        augmented = augmented / np.max(np.abs(augmented)) * 0.95
        return augmented
    
    def add_background_noise(self, audio: np.ndarray, noise_audio: np.ndarray,
                            snr_db: float = 15.0) -> np.ndarray:
        """
        Add background noise at specified SNR.
        
        Args:
            audio: Input audio signal
            noise_audio: Noise audio signal
            snr_db: Signal-to-noise ratio in dB (default: 15.0)
        
        Returns:
            Audio with background noise
        """
        # Ensure noise is same length as audio
        if len(noise_audio) < len(audio):
            # Repeat noise if too short
            repeats = int(np.ceil(len(audio) / len(noise_audio)))
            noise_audio = np.tile(noise_audio, repeats)
        
        # Trim noise to match audio length
        noise_audio = noise_audio[:len(audio)]
        
        # Calculate signal and noise power
        signal_power = np.mean(audio ** 2)
        noise_power = np.mean(noise_audio ** 2)
        
        # Calculate noise scaling factor for desired SNR
        snr_linear = 10 ** (snr_db / 10.0)
        noise_scale = np.sqrt(signal_power / (noise_power * snr_linear))
        
        # Add scaled noise
        augmented = audio + noise_scale * noise_audio
        
        # Normalize to prevent clipping
        augmented = augmented / np.max(np.abs(augmented)) * 0.95
        
        return augmented
    
    def volume_perturbation(self, audio: np.ndarray, gain_db: float) -> np.ndarray:
        """
        Change audio volume.
        
        Args:
            audio: Input audio signal
            gain_db: Gain in decibels (negative = quieter, positive = louder)
        
        Returns:
            Volume-adjusted audio
        """
        gain_linear = 10 ** (gain_db / 20.0)
        augmented = audio * gain_linear
        # Prevent clipping
        if np.max(np.abs(augmented)) > 1.0:
            augmented = augmented / np.max(np.abs(augmented)) * 0.95
        return augmented
    
    def augment_audio(self, audio_path: str, output_dir: Path,
                     techniques: List[str]) -> List[Tuple[str, str]]:
        """
        Apply augmentation techniques to audio file.
        
        Args:
            audio_path: Path to input audio
            output_dir: Directory to save augmented audio
            techniques: List of techniques to apply
        
        Returns:
            List of (output_path, augmentation_type) tuples
        """
        # Load audio
        audio, sr = librosa.load(audio_path, sr=self.sr, mono=True)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        base_name = Path(audio_path).stem
        
        augmented_files = []
        
        # Original file
        original_out = output_dir / f"{base_name}_original.wav"
        sf.write(str(original_out), audio, sr)
        augmented_files.append((str(original_out), "original"))
        
        # Speed perturbation
        if "speed" in techniques:
            for speed in [0.9, 1.1]:
                aug_audio = self.speed_perturbation(audio, speed)
                out_path = output_dir / f"{base_name}_speed{speed}.wav"
                sf.write(str(out_path), aug_audio, sr)
                augmented_files.append((str(out_path), f"speed_{speed}"))
        
        # White noise
        if "noise" in techniques:
            for noise_level in [0.003, 0.007]:
                aug_audio = self.add_white_noise(audio, noise_level)
                out_path = output_dir / f"{base_name}_noise{noise_level}.wav"
                sf.write(str(out_path), aug_audio, sr)
                augmented_files.append((str(out_path), f"noise_{noise_level}"))
        
        # Volume perturbation
        if "volume" in techniques:
            for gain in [-3, 3]:
                aug_audio = self.volume_perturbation(audio, gain)
                out_path = output_dir / f"{base_name}_vol{gain}db.wav"
                sf.write(str(out_path), aug_audio, sr)
                augmented_files.append((str(out_path), f"volume_{gain}db"))
        
        return augmented_files


def augment_dataset(input_tsv: str, output_tsv: str, output_audio_dir: str,
                   techniques: List[str], augment_ratio: float = 0.5):
    """
    Augment entire dataset.
    
    Args:
        input_tsv: Input TSV file (path, transcript, speaker, locale)
        output_tsv: Output TSV file with augmented data
        output_audio_dir: Directory to save augmented audio
        techniques: List of augmentation techniques
        augment_ratio: Fraction of samples to augment (0.0 to 1.0)
    """
    augmenter = AudioAugmenter()
    output_audio_path = Path(output_audio_dir)
    
    # Read input data
    samples = []
    with open(input_tsv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        samples = list(reader)
    
    print(f"Loaded {len(samples)} samples from {input_tsv}")
    
    # Select samples to augment
    num_to_augment = int(len(samples) * augment_ratio)
    samples_to_augment = random.sample(samples, num_to_augment)
    
    print(f"Augmenting {num_to_augment} samples...")
    
    # Augment selected samples
    augmented_samples = []
    
    for sample in tqdm(samples_to_augment, desc="Augmenting"):
        audio_path = sample["path"]
        transcript = sample["transcript"]
        speaker = sample["speaker"]
        locale = sample["locale"]
        
        # Generate augmented versions
        aug_files = augmenter.augment_audio(
            audio_path,
            output_audio_path / speaker,
            techniques
        )
        
        # Add augmented samples
        for aug_path, aug_type in aug_files:
            augmented_samples.append({
                "path": aug_path,
                "transcript": transcript,
                "speaker": f"{speaker}_{aug_type}",
                "locale": locale
            })
    
    # Combine original and augmented
    all_samples = samples + augmented_samples
    
    print(f"Total samples after augmentation: {len(all_samples)}")
    
    # Save to output TSV
    output_path = Path(output_tsv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["path", "transcript", "speaker", "locale"],
                               delimiter='\t')
        writer.writeheader()
        writer.writerows(all_samples)
    
    print(f"✓ Saved augmented dataset to {output_tsv}")


def main():
    parser = argparse.ArgumentParser(
        description="Augment Bengali ASR dataset"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input TSV file"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output TSV file"
    )
    parser.add_argument(
        "--output_audio_dir",
        type=str,
        default="./augmented/audio",
        help="Directory to save augmented audio"
    )
    parser.add_argument(
        "--speed_perturbation",
        action="store_true",
        help="Apply speed perturbation (0.9x, 1.1x)"
    )
    parser.add_argument(
        "--noise_injection",
        action="store_true",
        help="Add white noise"
    )
    parser.add_argument(
        "--volume_augmentation",
        action="store_true",
        help="Apply volume changes"
    )
    parser.add_argument(
        "--augment_ratio",
        type=float,
        default=0.5,
        help="Fraction of samples to augment (default: 0.5)"
    )
    
    args = parser.parse_args()
    
    # Determine techniques to apply
    techniques = []
    if args.speed_perturbation:
        techniques.append("speed")
    if args.noise_injection:
        techniques.append("noise")
    if args.volume_augmentation:
        techniques.append("volume")
    
    if not techniques:
        print("Warning: No augmentation techniques selected!")
        print("Use --speed_perturbation, --noise_injection, or --volume_augmentation")
        return
    
    print("\n" + "="*60)
    print("Bengali ASR Data Augmentation")
    print("="*60)
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Techniques: {', '.join(techniques)}")
    print(f"Augmentation ratio: {args.augment_ratio}")
    print("="*60 + "\n")
    
    augment_dataset(
        args.input,
        args.output,
        args.output_audio_dir,
        techniques,
        args.augment_ratio
    )
    
    print("\n✓ Augmentation complete!")


if __name__ == "__main__":
    main()
