import streamlit as st
import tempfile
from evaluate.pronunciation import pronunciation_score
from evaluate.grammar import correct_grammar


def main():
    st.title("Evaluate Your English")
    st.write("Upload an audio file and optionally a reference text to evaluate your pronunciation and grammar.")

    audio_file = st.file_uploader("Audio file", type=["wav", "mp3", "m4a"])
    reference_text = st.text_input("Reference text (optional)")

    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            audio_path = tmp.name

        st.audio(audio_file)

        if st.button("Transcribe and Evaluate"):
            st.info("Processing...")
            score = pronunciation_score(audio_path, reference_text or "")
            st.write(f"Pronunciation Score: {score:.2f}")

            transcription = correct_grammar(reference_text) if reference_text else ""
            if transcription:
                st.write("Grammar Correction:")
                st.write(transcription)


if __name__ == "__main__":
    main()
