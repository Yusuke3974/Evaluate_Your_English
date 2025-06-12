import sys
import os
import types
import contextlib

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create dummy torch module to avoid heavy dependency
sys.modules['torch'] = types.SimpleNamespace(no_grad=lambda: contextlib.nullcontext())
# Provide dummy external modules required by the package
sys.modules['phonemizer'] = types.SimpleNamespace(phonemize=lambda *a, **k: "")
sys.modules['faster_whisper'] = types.SimpleNamespace(WhisperModel=object)
sys.modules['editdistance'] = types.SimpleNamespace(eval=lambda *a, **k: 0)
sys.modules['transformers'] = types.ModuleType('transformers')
sys.modules['transformers'].AutoModelForSeq2SeqLM = object
sys.modules['transformers'].AutoTokenizer = object
sys.modules['numpy'] = types.ModuleType('numpy')

from evaluate import pronunciation
from evaluate import grammar


def test_pronunciation_score(monkeypatch):
    monkeypatch.setattr(pronunciation, 'load_whisper_model', lambda model_size='base': 'model')
    def fake_transcribe(model, audio_path):
        assert model == 'model'
        return 'hello world'
    monkeypatch.setattr(pronunciation, 'transcribe_audio', fake_transcribe)
    monkeypatch.setattr(pronunciation, 'phonemize', lambda text, language='en-us': text)
    score = pronunciation.pronunciation_score('dummy.wav', 'hello world')
    assert score == 1.0


class DummyTokenizer:
    def __call__(self, text, return_tensors='pt'):
        return {}
    def decode(self, ids, skip_special_tokens=True):
        return 'corrected'

class DummyModel:
    def generate(self, **inputs):
        return [[1]]


def test_correct_grammar(monkeypatch):
    dummy_tokenizer = DummyTokenizer()
    dummy_model = DummyModel()
    monkeypatch.setattr(grammar, 'load_model', lambda: (dummy_tokenizer, dummy_model))
    result = grammar.correct_grammar('text with error')
    assert result == 'corrected'


def test_correct_grammar_cached(monkeypatch):
    counter = {'tokenizer': 0, 'model': 0}

    class DummyTokenizer:
        def __call__(self, text, return_tensors='pt'):
            return {}

        def decode(self, ids, skip_special_tokens=True):
            return 'ok'

    class DummyModel:
        def generate(self, **inputs):
            return [[1]]

    def fake_tokenizer_from_pretrained(name):
        counter['tokenizer'] += 1
        return DummyTokenizer()

    def fake_model_from_pretrained(name):
        counter['model'] += 1
        return DummyModel()

    monkeypatch.setattr(grammar, 'AutoTokenizer', types.SimpleNamespace(from_pretrained=fake_tokenizer_from_pretrained))
    monkeypatch.setattr(grammar, 'AutoModelForSeq2SeqLM', types.SimpleNamespace(from_pretrained=fake_model_from_pretrained))
    grammar.load_model.cache_clear()

    assert grammar.correct_grammar('one') == 'ok'
    assert grammar.correct_grammar('two') == 'ok'
    assert counter['tokenizer'] == 1
    assert counter['model'] == 1


def test_pronunciation_score_cached(monkeypatch):
    counter = {'model': 0}

    class DummyWhisperModel:
        def __init__(self, size):
            counter['model'] += 1

    def fake_transcribe(model, audio_path):
        assert isinstance(model, DummyWhisperModel)
        return 'hello world'

    monkeypatch.setattr(pronunciation, 'WhisperModel', DummyWhisperModel)
    monkeypatch.setattr(pronunciation, 'phonemize', lambda text, language='en-us': text)
    monkeypatch.setattr(pronunciation, 'transcribe_audio', fake_transcribe)
    pronunciation.load_whisper_model.cache_clear()

    pronunciation.pronunciation_score('a.wav', 'hello world')
    pronunciation.pronunciation_score('b.wav', 'hello world')
    assert counter['model'] == 1
