import streamlit as st
import tempfile
from evaluate.pronunciation import pronunciation_score
from evaluate.grammar import correct_grammar
from streamlit_audiorecorder import audiorecorder


def main():
    st.title("Evaluate Your English")
    st.write(
        "Upload an audio file or record directly and optionally provide a reference text to evaluate your pronunciation and grammar."
    )

    method = st.radio("Input method", ["Upload audio file", "Record audio"])
    audio_path = None

    if method == "Upload audio file":
        audio_file = st.file_uploader("Audio file", type=["wav", "mp3", "m4a"])
        if audio_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                audio_path = tmp.name
            st.audio(audio_file)
    else:
        audio_bytes = audiorecorder(
            start_prompt="Click to record",
            stop_prompt="Click to stop",
            pause_prompt="Recording...",
        )
        if audio_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_bytes)
                audio_path = tmp.name
            st.audio(audio_bytes)

    reference_text = st.text_input("Reference text (optional)")

    if audio_path and st.button("Transcribe and Evaluate"):
        st.info("Processing...")
        score = pronunciation_score(audio_path, reference_text or "")
        st.write(f"Pronunciation Score: {score:.2f}")

        transcription = correct_grammar(reference_text) if reference_text else ""
        if transcription:
            st.write("Grammar Correction:")
            st.write(transcription)


if __name__ == "__main__":
    main()
