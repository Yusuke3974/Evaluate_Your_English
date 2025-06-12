# Evaluate Your English

This app provides three core features:

1. **English Pronunciation Evaluation** using a Whisper ASR model and phoneme comparison.
2. **English Grammar Correction** using a transformer model.
3. **English Text Level Assessment** based on Flesch readability metrics. This feature works on any text input, independent of the audio tools.

Both the grammar and pronunciation models are cached so they only load once per
process. This significantly speeds up repeated evaluations.

The application is built with **Streamlit** and relies on the following libraries:

- `faster-whisper` for speech to text
- `phonemizer` and `editdistance` for pronunciation scoring
- `transformers` and `torch` for grammar correction
- `streamlit-audiorecorder` for microphone input

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

## Text Level Assessment

Use the dedicated text box in the app to evaluate the readability of any text.
The results display Flesch Reading Ease and Flesch–Kincaid Grade Level.
