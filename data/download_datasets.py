"""
Download public Bengali ASR datasets for model training.

Datasets:
1. OpenSLR SLR53 - Bengali ASR training data corpus
2. Mozilla Common Voice (bn) - Community-contributed Bengali speech
3. Bengali.AI Speech Recognition Dataset

Usage:
    python download_datasets.py --datasets openslr common_voice bengaliai --output ./raw

Author: BRAC Data Science Team
Date: October 2025
"""

import argparse
import json
import os
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import List, Dict
from urllib.request import urlretrieve

try:
    from datasets import load_dataset
    from tqdm import tqdm
    import requests
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "datasets", "tqdm", "requests"])
    from datasets import load_dataset
    from tqdm import tqdm
    import requests


class DatasetDownloader:
    """Handles downloading and organizing Bengali ASR datasets."""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_dir = self.output_dir.parent / "manifests"
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        
    def download_openslr_slr53(self):
        """
        Download OpenSLR SLR53 Bengali dataset.
        
        Dataset info:
        - URL: https://www.openslr.org/53/
        - Size: ~14GB compressed
        - Content: ~196 hours of read Bengali speech
        """
        print("\n" + "="*60)
        print("Downloading OpenSLR SLR53 Dataset")
        print("="*60)
        
        dataset_dir = self.output_dir / "openslr_slr53"
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        # OpenSLR SLR53 data URLs
        # TODO: Verify these URLs are current
        base_url = "https://www.openslr.org/resources/53"
        files = [
            "asr_bengali_train.tar.gz",
            "asr_bengali_valid.tar.gz",
            "asr_bengali_test.tar.gz"
        ]
        
        manifest = {
            "dataset_name": "openslr_slr53",
            "source_url": "https://www.openslr.org/53/",
            "description": "Bengali ASR training data corpus",
            "language": "bn",
            "total_hours": 196,
            "files": []
        }
        
        for filename in files:
            file_url = f"{base_url}/{filename}"
            output_path = dataset_dir / filename
            
            if output_path.exists():
                print(f"✓ {filename} already exists, skipping...")
                continue
            
            print(f"Downloading {filename}...")
            try:
                # Download with progress bar
                response = requests.get(file_url, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                
                with open(output_path, 'wb') as f, tqdm(
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        size = f.write(chunk)
                        pbar.update(size)
                
                # Extract
                print(f"Extracting {filename}...")
                with tarfile.open(output_path, 'r:gz') as tar:
                    tar.extractall(path=dataset_dir)
                
                manifest["files"].append({
                    "filename": filename,
                    "size_bytes": output_path.stat().st_size,
                    "extracted": True
                })
                
                print(f"✓ {filename} downloaded and extracted successfully")
                
            except Exception as e:
                print(f"✗ Error downloading {filename}: {str(e)}")
                print("  You may need to download this manually from:")
                print(f"  {file_url}")
                continue
        
        # Save manifest
        manifest_path = self.manifest_dir / "openslr_slr53.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ OpenSLR SLR53 setup complete")
        print(f"  Location: {dataset_dir}")
        print(f"  Manifest: {manifest_path}")
        
        return dataset_dir
    
    def download_common_voice(self):
        """
        Download Mozilla Common Voice Bengali dataset using Hugging Face datasets.
        
        Dataset info:
        - URL: https://commonvoice.mozilla.org/bn
        - Requires: Hugging Face account and dataset access agreement
        """
        print("\n" + "="*60)
        print("Downloading Mozilla Common Voice (bn) Dataset")
        print("="*60)
        
        dataset_dir = self.output_dir / "common_voice_bn"
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        print("\nNOTE: You may need to:")
        print("  1. Create a Hugging Face account at https://huggingface.co/")
        print("  2. Accept the Common Voice dataset terms at:")
        print("     https://huggingface.co/datasets/mozilla-foundation/common_voice_13_0")
        print("  3. Log in via: huggingface-cli login")
        print()
        
        try:
            print("Loading dataset from Hugging Face...")
            # Load Common Voice dataset (Bengali)
            dataset = load_dataset(
                "mozilla-foundation/common_voice_13_0",
                "bn",
                cache_dir=str(dataset_dir),
                trust_remote_code=True
            )
            
            print(f"✓ Dataset loaded successfully")
            print(f"  Train samples: {len(dataset['train'])}")
            print(f"  Validation samples: {len(dataset['validation'])}")
            print(f"  Test samples: {len(dataset['test'])}")
            
            # Create manifest
            manifest = {
                "dataset_name": "common_voice_bn",
                "source_url": "https://commonvoice.mozilla.org/bn",
                "description": "Community-contributed Bengali speech",
                "language": "bn",
                "splits": {
                    "train": len(dataset['train']),
                    "validation": len(dataset['validation']),
                    "test": len(dataset['test'])
                },
                "total_samples": sum([
                    len(dataset['train']),
                    len(dataset['validation']),
                    len(dataset['test'])
                ])
            }
            
            manifest_path = self.manifest_dir / "common_voice_bn.json"
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Common Voice download complete")
            print(f"  Location: {dataset_dir}")
            print(f"  Manifest: {manifest_path}")
            
            return dataset_dir
            
        except Exception as e:
            print(f"✗ Error downloading Common Voice: {str(e)}")
            print("\nTroubleshooting:")
            print("  - Run: huggingface-cli login")
            print("  - Accept dataset terms at the URL above")
            print("  - Check internet connection")
            return None
    
    def download_bengaliai(self):
        """
        Download Bengali.AI Speech Recognition dataset.
        
        Dataset info:
        - URL: https://huggingface.co/datasets/BengaliAI/bengali_speech
        - Contains diverse Bengali dialects
        """
        print("\n" + "="*60)
        print("Downloading Bengali.AI Speech Dataset")
        print("="*60)
        
        dataset_dir = self.output_dir / "bengaliai"
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            print("Loading dataset from Hugging Face...")
            # TODO: Update with actual Bengali.AI dataset name when available
            # This is a placeholder - adjust based on actual dataset
            dataset = load_dataset(
                "BengaliAI/bengali_speech",
                cache_dir=str(dataset_dir),
                trust_remote_code=True
            )
            
            print(f"✓ Dataset loaded successfully")
            
            # Create manifest
            manifest = {
                "dataset_name": "bengaliai_speech",
                "source_url": "https://huggingface.co/datasets/BengaliAI/bengali_speech",
                "description": "Bengali.AI diverse dialects dataset",
                "language": "bn",
                "splits": {split: len(dataset[split]) for split in dataset.keys()},
                "total_samples": sum([len(dataset[split]) for split in dataset.keys()])
            }
            
            manifest_path = self.manifest_dir / "bengaliai.json"
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Bengali.AI download complete")
            print(f"  Location: {dataset_dir}")
            print(f"  Manifest: {manifest_path}")
            
            return dataset_dir
            
        except Exception as e:
            print(f"✗ Error downloading Bengali.AI dataset: {str(e)}")
            print("\nNote: This dataset may not be publicly available yet.")
            print("Check https://bengali.ai/ for latest datasets.")
            return None


def main():
    parser = argparse.ArgumentParser(
        description="Download Bengali ASR datasets for model training"
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=["openslr", "common_voice", "bengaliai", "all"],
        default=["all"],
        help="Which datasets to download (default: all)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./raw",
        help="Output directory for downloaded datasets (default: ./raw)"
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip datasets that already exist"
    )
    
    args = parser.parse_args()
    
    # Expand "all" option
    if "all" in args.datasets:
        args.datasets = ["openslr", "common_voice", "bengaliai"]
    
    print("\n" + "="*60)
    print("Bengali ASR Dataset Downloader")
    print("="*60)
    print(f"Output directory: {args.output}")
    print(f"Datasets to download: {', '.join(args.datasets)}")
    print("="*60)
    
    downloader = DatasetDownloader(args.output)
    results = {}
    
    # Download each dataset
    if "openslr" in args.datasets:
        results["openslr"] = downloader.download_openslr_slr53()
    
    if "common_voice" in args.datasets:
        results["common_voice"] = downloader.download_common_voice()
    
    if "bengaliai" in args.datasets:
        results["bengaliai"] = downloader.download_bengaliai()
    
    # Summary
    print("\n" + "="*60)
    print("Download Summary")
    print("="*60)
    for dataset, path in results.items():
        status = "✓ SUCCESS" if path else "✗ FAILED"
        print(f"{dataset:20s}: {status}")
    
    print("\nNext steps:")
    print("  1. Verify downloaded datasets")
    print("  2. Run preprocessing: python preprocess.py")
    print("  3. Check manifests in: data/manifests/")
    print()


if __name__ == "__main__":
    main()
