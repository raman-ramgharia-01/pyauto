import streamlit as st
from groq_transcriber import transcribe_audio_with_groq

def main():
    audio_bytes = st.audio_input("Click to record your question", key="audio_input")
    if audio_bytes is not None:
        st.write("Audio recorded successfully. Processing...")
        transcribed_text = transcribe_audio_with_groq(audio_bytes)
        st.write(f"Transcribed Text: {transcribed_text}")
if __name__ == "__main__":
    main()