# Evaluate Your English

This app provides two core features:

1. **English Pronunciation Evaluation** using a Whisper ASR model and phoneme comparison.
2. **English Grammar Correction** using a transformer model.

The application is built with **Streamlit** and relies on the following libraries:

- `faster-whisper` for speech to text
- `phonemizer` and `editdistance` for pronunciation scoring
- `transformers` and `torch` for grammar correction

## Setup

Install the dependencies using [Poetry](https://python-poetry.org):

```bash
poetry install
```

If you prefer using `pip`, an exported `requirements.txt` is also provided:

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

Upload an audio file (wav/mp3/m4a) and, optionally, a reference text. The app will output a pronunciation score and grammar correction suggestions.
