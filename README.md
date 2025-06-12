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

If you encounter errors related to `torch.classes` when launching the
app, `app.py` attempts to patch Streamlit's file watcher to skip this
module. The patch is optional and is automatically skipped when the
watcher implementation doesn't expose the required hook. This
workaround avoids a startup crash caused by
`streamlit.watcher.local_sources_watcher` failing on
`torch.classes`.
## Text Level Assessment

Use the dedicated text box in the app to evaluate the readability of any text.
The results display Flesch Reading Ease and Flesch–Kincaid Grade Level.
