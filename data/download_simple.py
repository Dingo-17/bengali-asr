#!/usr/bin/env python3
"""
Simplified Bengali dataset downloader using only publicly accessible datasets
"""

import os
import sys
from pathlib import Path

def setup_directories():
    """Create necessary directories"""
    base_dir = Path(__file__).parent
    dirs = [
        base_dir / "raw",
        base_dir / "processed",
        base_dir / "manifests",
        base_dir / "brac_dialect",
        base_dir / "brac_corrections"
    ]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    print("✓ Directories created")

def download_mozilla_common_voice():
    """Download Mozilla Common Voice with proper authentication"""
    try:
        from datasets import load_dataset
        
        print("\n" + "="*60)
        print("Downloading Mozilla Common Voice (Bengali)")
        print("="*60)
        print("\nNOTE: This requires:")
        print("  1. Hugging Face account: https://huggingface.co/join")
        print("  2. Accept terms: https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0")
        print("  3. Login: huggingface-cli login\n")
        
        response = input("Have you completed the above steps? (y/n): ")
        if response.lower() != 'y':
            print("⚠️  Skipping Common Voice download")
            print("   Complete the steps above and run this script again")
            return False
        
        print("\nDownloading Common Voice Bengali (this may take a while)...")
        
        # Try newer version first
        try:
            dataset = load_dataset(
                "mozilla-foundation/common_voice_17_0",
                "bn",
                split="train+validation+test"
            )
            print(f"✓ Downloaded {len(dataset)} samples")
            
            # Save to disk
            output_dir = Path(__file__).parent / "raw" / "common_voice_bn"
            output_dir.mkdir(parents=True, exist_ok=True)
            dataset.save_to_disk(str(output_dir))
            print(f"✓ Saved to {output_dir}")
            return True
            
        except Exception as e:
            print(f"✗ Error with v17: {e}")
            print("Trying version 16...")
            
            dataset = load_dataset(
                "mozilla-foundation/common_voice_16_0",
                "bn",
                split="train+validation+test"
            )
            print(f"✓ Downloaded {len(dataset)} samples")
            
            output_dir = Path(__file__).parent / "raw" / "common_voice_bn"
            output_dir.mkdir(parents=True, exist_ok=True)
            dataset.save_to_disk(str(output_dir))
            print(f"✓ Saved to {output_dir}")
            return True
            
    except Exception as e:
        print(f"✗ Error downloading Common Voice: {e}")
        return False

def download_openslr_manual_guide():
    """Provide manual download instructions for OpenSLR"""
    print("\n" + "="*60)
    print("OpenSLR SLR53 - Manual Download Required")
    print("="*60)
    print("\nThe OpenSLR URLs have changed. Please download manually:")
    print("\n1. Visit: https://www.openslr.org/53/")
    print("2. Download these files:")
    print("   - asr_bengali_train.tar.gz")
    print("   - asr_bengali_valid.tar.gz") 
    print("   - asr_bengali_test.tar.gz")
    print("\n3. Extract them to:")
    print(f"   {Path(__file__).parent / 'raw' / 'openslr_slr53'}/")
    print("\nOr use this command:")
    print("   cd data/raw && mkdir -p openslr_slr53 && cd openslr_slr53")
    print("   # Download files to this directory")
    print("   tar -xzf asr_bengali_train.tar.gz")
    print("   tar -xzf asr_bengali_valid.tar.gz")
    print("   tar -xzf asr_bengali_test.tar.gz")

def create_sample_data():
    """Create sample Bengali data for testing"""
    print("\n" + "="*60)
    print("Creating Sample Test Data")
    print("="*60)
    
    sample_dir = Path(__file__).parent / "raw" / "sample_bengali"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a sample manifest
    manifest_file = sample_dir / "manifest.txt"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        f.write("# Sample Bengali transcripts for testing\n")
        f.write("# Format: filename\ttranscript\tspeaker\n")
        f.write("sample_001.wav\tআমি বাংলায় কথা বলি\tspeaker_001\n")
        f.write("sample_002.wav\tএটি একটি পরীক্ষা\tspeaker_001\n")
        f.write("sample_003.wav\tবাংলাদেশ আমার দেশ\tspeaker_002\n")
    
    print(f"✓ Sample data created at: {sample_dir}")
    print("  You can use this for testing the pipeline")

def main():
    print("="*60)
    print("Bengali ASR Simple Dataset Downloader")
    print("="*60)
    
    # Setup directories
    setup_directories()
    
    # Download datasets
    print("\nWhich datasets would you like to download?")
    print("1. Mozilla Common Voice (requires HF login)")
    print("2. OpenSLR SLR53 (manual download instructions)")
    print("3. Create sample test data")
    print("4. All of the above")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice in ['1', '4']:
        download_mozilla_common_voice()
    
    if choice in ['2', '4']:
        download_openslr_manual_guide()
    
    if choice in ['3', '4']:
        create_sample_data()
    
    print("\n" + "="*60)
    print("Download Process Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. If using Common Voice, verify data in: data/raw/common_voice_bn")
    print("2. If using OpenSLR, complete manual download")
    print("3. Run preprocessing: python3 data/preprocess.py")
    print("\nFor help, see: TROUBLESHOOTING.md")

if __name__ == "__main__":
    main()
