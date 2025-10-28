"""
Training utilities for Bengali ASR.

Includes:
- Text normalization functions
- Custom data collators
- Metric computation helpers
- Tokenizer/processor creation utilities

Author: BRAC Data Science Team
Date: October 2025
"""

import re
import unicodedata
from typing import Dict, List, Optional

try:
    from bnlp import BengaliNormalizer
    BNLP_AVAILABLE = True
except ImportError:
    BNLP_AVAILABLE = False
    print("Warning: bnlp-toolkit not available. Install with: pip install bnlp-toolkit")


class BengaliTextNormalizer:
    """Normalize Bengali text for ASR training."""
    
    def __init__(self, remove_punctuation: bool = False, 
                 normalize_numbers: bool = True,
                 unicode_normalize: bool = True):
        """
        Initialize normalizer.
        
        Args:
            remove_punctuation: Remove punctuation marks
            normalize_numbers: Convert numbers to words
            unicode_normalize: Apply Unicode NFKC normalization
        """
        self.remove_punctuation = remove_punctuation
        self.normalize_numbers = normalize_numbers
        self.unicode_normalize = unicode_normalize
        
        if BNLP_AVAILABLE:
            self.bnlp_normalizer = BengaliNormalizer()
        
        # Bengali number mappings
        self.bengali_digits = {
            '০': 'শূন্য', '১': 'এক', '২': 'দুই', '৩': 'তিন',
            '৪': 'চার', '৫': 'পাঁচ', '৬': 'ছয়', '৭': 'সাত',
            '৮': 'আট', '৯': 'নয়'
        }
        
        # Common punctuation to remove
        self.punctuation = '।!,;?:—–-()[]{}""\'\'`´'
    
    def normalize(self, text: str) -> str:
        """
        Apply all normalization steps.
        
        Args:
            text: Input text
        
        Returns:
            Normalized text
        """
        # Unicode normalization
        if self.unicode_normalize:
            text = unicodedata.normalize('NFKC', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Normalize numbers
        if self.normalize_numbers:
            text = self._normalize_bengali_numbers(text)
        
        # Remove punctuation
        if self.remove_punctuation:
            for punct in self.punctuation:
                text = text.replace(punct, '')
        
        # Use bnlp normalizer if available
        if BNLP_AVAILABLE:
            text = self.bnlp_normalizer(text)
        
        # Final cleanup
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _normalize_bengali_numbers(self, text: str) -> str:
        """
        Convert Bengali digits to words.
        
        Args:
            text: Input text with Bengali digits
        
        Returns:
            Text with digits converted to words
        """
        # Simple digit-by-digit conversion
        # TODO: Implement proper number-to-word conversion for multi-digit numbers
        for digit, word in self.bengali_digits.items():
            text = text.replace(digit, f' {word} ')
        
        return text
    
    def normalize_batch(self, texts: List[str]) -> List[str]:
        """
        Normalize a batch of texts.
        
        Args:
            texts: List of input texts
        
        Returns:
            List of normalized texts
        """
        return [self.normalize(text) for text in texts]


def create_vocab_from_text(texts: List[str], 
                          add_special_tokens: bool = True) -> Dict[str, int]:
    """
    Create vocabulary from text corpus.
    
    Args:
        texts: List of text strings
        add_special_tokens: Whether to add [UNK], [PAD] tokens
    
    Returns:
        Dictionary mapping characters to IDs
    """
    # Extract all unique characters
    all_chars = set()
    for text in texts:
        all_chars.update(set(text))
    
    # Sort for consistency
    sorted_chars = sorted(list(all_chars))
    
    # Create vocab dict
    vocab = {char: idx for idx, char in enumerate(sorted_chars)}
    
    # Add special tokens
    if add_special_tokens:
        vocab['[UNK]'] = len(vocab)
        vocab['[PAD]'] = len(vocab)
        vocab['|'] = len(vocab)  # Word delimiter
    
    return vocab


def calculate_wer(predictions: List[str], references: List[str]) -> float:
    """
    Calculate Word Error Rate (WER).
    
    Args:
        predictions: List of predicted transcripts
        references: List of reference transcripts
    
    Returns:
        WER as percentage
    """
    try:
        from jiwer import wer
        return wer(references, predictions)
    except ImportError:
        print("Warning: jiwer not installed. Install with: pip install jiwer")
        return 0.0


def calculate_cer(predictions: List[str], references: List[str]) -> float:
    """
    Calculate Character Error Rate (CER).
    
    Args:
        predictions: List of predicted transcripts
        references: List of reference transcripts
    
    Returns:
        CER as percentage
    """
    try:
        from jiwer import cer
        return cer(references, predictions)
    except ImportError:
        print("Warning: jiwer not installed. Install with: pip install jiwer")
        return 0.0


# Example usage
if __name__ == "__main__":
    # Test normalizer
    normalizer = BengaliTextNormalizer()
    
    test_texts = [
        "আমি বাংলায় কথা বলি।",
        "আজ ১০ তারিখ।",
        "এটি  একটি   পরীক্ষা।"
    ]
    
    print("Text Normalization Examples:")
    print("="*60)
    for text in test_texts:
        normalized = normalizer.normalize(text)
        print(f"Original:   {text}")
        print(f"Normalized: {normalized}")
        print()
