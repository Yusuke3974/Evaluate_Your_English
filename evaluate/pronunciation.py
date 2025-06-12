from phonemizer import phonemize
from faster_whisper import WhisperModel


def load_whisper_model(model_size="base"):
    """Load a Whisper ASR model."""
    return WhisperModel(model_size)


def transcribe_audio(model, audio_path):
    segments, _ = model.transcribe(audio_path)
    return "".join([seg.text for seg in segments])


def pronunciation_score(audio_path: str, reference_text: str, model_size="base") -> float:
    """Approximate pronunciation score using phoneme error rate."""
    asr_model = load_whisper_model(model_size)
    predicted_text = transcribe_audio(asr_model, audio_path)

    ref_phonemes = phonemize(reference_text, language="en-us")
    pred_phonemes = phonemize(predicted_text, language="en-us")

    ref_tokens = ref_phonemes.split()
    pred_tokens = pred_phonemes.split()

    # simple edit distance
    import editdistance

    distance = editdistance.eval(ref_tokens, pred_tokens)
    max_len = max(len(ref_tokens), len(pred_tokens))
    if max_len == 0:
        return 0.0
    return 1.0 - distance / max_len
