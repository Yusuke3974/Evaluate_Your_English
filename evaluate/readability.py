import re

VOWELS = "aeiouy"


def count_syllables(word: str) -> int:
    """Rudimentary syllable count used for readability metrics."""
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    syllables = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            syllables += 1
        prev_vowel = is_vowel
    if word.endswith("e") and syllables > 1:
        syllables -= 1
    return syllables or 1


def evaluate_text_level(text: str) -> dict:
    """Return Flesch Reading Ease and Flesch–Kincaid Grade Level for the text."""
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"\b\w+\b", text.lower())
    if not sentences or not words:
        return {"flesch_reading_ease": 0.0, "flesch_kincaid_grade": 0.0}

    total_sentences = len(sentences)
    total_words = len(words)
    total_syllables = sum(count_syllables(w) for w in words)

    words_per_sentence = total_words / total_sentences
    syllables_per_word = total_syllables / total_words

    reading_ease = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
    grade_level = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59

    return {
        "flesch_reading_ease": reading_ease,
        "flesch_kincaid_grade": grade_level,
    }
