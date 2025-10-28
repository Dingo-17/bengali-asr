"""
Transliteration utilities for Bengali ASR.

This module provides transliteration between:
1. Bengali script → IPA (International Phonetic Alphabet)
2. Bengali script → Latin/Roman script
3. IPA → Bengali script (candidate generation)

Uses:
- Epitran for G2P (Grapheme-to-Phoneme)
- Aksharamukha for script conversion

Usage:
    from transliterate import bengali_to_latin, bengali_to_ipa, latin_to_bengali
    
    text = "আমি বাংলায় কথা বলি"
    latin = bengali_to_latin(text)  # "ami banglay kotha boli"
    ipa = bengali_to_ipa(text)      # IPA representation

Author: BRAC Data Science Team
Date: October 2025
"""

from typing import List, Tuple, Optional

try:
    import epitran
    EPITRAN_AVAILABLE = True
except ImportError:
    EPITRAN_AVAILABLE = False
    print("Warning: epitran not available. Install with: pip install epitran")

try:
    from aksharamukha import transliterate as ak_transliterate
    AKSHARAMUKHA_AVAILABLE = True
except ImportError:
    AKSHARAMUKHA_AVAILABLE = False
    print("Warning: aksharamukha not available. Install with: pip install aksharamukha")


class BengaliTransliterator:
    """Handle Bengali transliteration tasks."""
    
    def __init__(self):
        """Initialize transliterators."""
        if EPITRAN_AVAILABLE:
            try:
                # Initialize Epitran for Bengali
                self.epi = epitran.Epitran('ben-Beng')
            except Exception as e:
                print(f"Warning: Could not initialize Epitran: {e}")
                self.epi = None
        else:
            self.epi = None
        
        # Fallback romanization table
        self.romanization_map = {
            # Vowels
            'অ': 'o', 'আ': 'a', 'ই': 'i', 'ঈ': 'i', 'উ': 'u', 'ঊ': 'u',
            'ঋ': 'ri', 'এ': 'e', 'ঐ': 'oi', 'ও': 'o', 'ঔ': 'ou',
            
            # Consonants
            'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
            'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'ny',
            'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
            'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
            'প': 'p', 'ফ': 'ph', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
            'য': 'j', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh',
            'স': 's', 'হ': 'h',
            
            # Special
            'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't', 'ং': 'ng', 'ঃ': 'h', 'ঁ': '',
            
            # Vowel marks
            'া': 'a', 'ি': 'i', 'ী': 'i', 'ু': 'u', 'ূ': 'u', 'ৃ': 'ri',
            'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou', '্': ''
        }
    
    def bengali_to_ipa(self, text: str) -> str:
        """
        Convert Bengali text to IPA.
        
        Args:
            text: Bengali text
        
        Returns:
            IPA transcription
        """
        if self.epi:
            try:
                return self.epi.transliterate(text)
            except Exception as e:
                print(f"Warning: Epitran conversion failed: {e}")
        
        # Fallback to simple romanization if Epitran not available
        return self.bengali_to_latin(text)
    
    def bengali_to_latin(self, text: str, scheme: str = "IAST") -> str:
        """
        Convert Bengali script to Latin/Roman script.
        
        Args:
            text: Bengali text
            scheme: Romanization scheme (IAST, ISO, etc.)
        
        Returns:
            Romanized text
        """
        if AKSHARAMUKHA_AVAILABLE:
            try:
                return ak_transliterate.process('Bengali', 'IAST', text)
            except Exception as e:
                print(f"Warning: Aksharamukha conversion failed: {e}")
        
        # Fallback to simple character mapping
        result = []
        for char in text:
            if char in self.romanization_map:
                result.append(self.romanization_map[char])
            else:
                result.append(char)
        
        return ''.join(result)
    
    def latin_to_bengali(self, text: str) -> str:
        """
        Convert Latin/Roman script to Bengali.
        
        Args:
            text: Romanized text (IAST or similar)
        
        Returns:
            Bengali text
        """
        if AKSHARAMUKHA_AVAILABLE:
            try:
                return ak_transliterate.process('IAST', 'Bengali', text)
            except Exception as e:
                print(f"Warning: Aksharamukha conversion failed: {e}")
        
        # No reliable fallback for reverse transliteration
        return text
    
    def latin_to_ipa(self, text: str) -> str:
        """
        Convert Latin script to IPA via Bengali.
        
        Args:
            text: Latin/Roman text
        
        Returns:
            IPA transcription
        """
        # First convert to Bengali
        bengali = self.latin_to_bengali(text)
        
        # Then to IPA
        return self.bengali_to_ipa(bengali)
    
    def generate_candidates(self, ipa: str, confidence_threshold: float = 0.7) -> List[Tuple[str, float]]:
        """
        Generate Bengali orthography candidates from IPA.
        
        This is useful when ASR confidence is low - we can generate
        multiple possible spellings and rank them.
        
        Args:
            ipa: IPA transcription
            confidence_threshold: Minimum confidence for candidates
        
        Returns:
            List of (bengali_text, confidence) tuples
        """
        # TODO: Implement proper candidate generation
        # This would require:
        # 1. IPA → phoneme mapping
        # 2. Phoneme → Bengali grapheme mapping (multiple possibilities)
        # 3. Language model scoring of candidates
        
        # For now, return single best-effort candidate
        candidates = []
        
        try:
            # Try reverse transliteration
            bengali = self.latin_to_bengali(ipa)
            candidates.append((bengali, 0.8))
        except Exception:
            pass
        
        return candidates


# Global instance
_transliterator = None


def get_transliterator() -> BengaliTransliterator:
    """Get singleton transliterator instance."""
    global _transliterator
    if _transliterator is None:
        _transliterator = BengaliTransliterator()
    return _transliterator


# Convenience functions
def bengali_to_latin(text: str) -> str:
    """Convert Bengali to Latin script."""
    return get_transliterator().bengali_to_latin(text)


def bengali_to_ipa(text: str) -> str:
    """Convert Bengali to IPA."""
    return get_transliterator().bengali_to_ipa(text)


def latin_to_bengali(text: str) -> str:
    """Convert Latin to Bengali script."""
    return get_transliterator().latin_to_bengali(text)


def latin_to_ipa(text: str) -> str:
    """Convert Latin to IPA via Bengali."""
    return get_transliterator().latin_to_ipa(text)


def transliterate_with_fallback(
    bengali_transcript: str,
    confidence: float,
    confidence_threshold: float = 0.7
) -> dict:
    """
    Transliterate with fallback when confidence is low.
    
    When primary ASR confidence < threshold, generate multiple
    candidate Bengali orthographies and return them for ranking.
    
    Args:
        bengali_transcript: Primary ASR output
        confidence: ASR confidence score
        confidence_threshold: Threshold for using fallback
    
    Returns:
        Dictionary with transliteration results
    """
    result = {
        "primary": bengali_transcript,
        "latin": bengali_to_latin(bengali_transcript),
        "ipa": bengali_to_ipa(bengali_transcript),
        "confidence": confidence,
        "candidates": []
    }
    
    # If confidence is low, generate alternatives
    if confidence < confidence_threshold:
        # Convert to IPA first
        ipa = bengali_to_ipa(bengali_transcript)
        
        # Generate candidates
        transliterator = get_transliterator()
        candidates = transliterator.generate_candidates(ipa, confidence_threshold)
        
        result["candidates"] = [
            {"text": text, "confidence": conf}
            for text, conf in candidates
        ]
    
    return result


# Example usage
if __name__ == "__main__":
    print("Bengali Transliteration Examples")
    print("="*60)
    
    test_text = "আমি বাংলায় কথা বলি"
    
    print(f"\nOriginal (Bengali): {test_text}")
    print(f"Latin: {bengali_to_latin(test_text)}")
    print(f"IPA: {bengali_to_ipa(test_text)}")
    
    # Test fallback with low confidence
    print("\nFallback transliteration (low confidence):")
    result = transliterate_with_fallback(test_text, confidence=0.6)
    print(f"Primary: {result['primary']}")
    print(f"Latin: {result['latin']}")
    print(f"IPA: {result['ipa']}")
    print(f"Candidates: {result['candidates']}")
