import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# UI Setup
st.title("🌍 Language Translation Tool")
st.write("Enter your text below to translate it into your language of choice.")

# Language Mapping
languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru"
}

# User Input
text = st.text_area("Enter Text", height=150)

# Source and Target Language Selection
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", ["auto"] + list(languages.keys()))
with col2:
    target_lang = st.selectbox("Target Language", list(languages.keys()))

if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text to translate.")
    else:
        try:
            # Determine source language code
            src_code = "auto" if source_lang == "auto" else languages[source_lang]
            tgt_code = languages[target_lang]

            # Send text to API and get translated response
            translated = GoogleTranslator(
                source=src_code,
                target=tgt_code
            ).translate(text)

            st.success("Translation Successful!")
            
            # Display translated text clearly
            st.markdown("### Translated Text:")
            st.write(translated)

            # Optional Feature 1: Copy Button (Native to st.code)[cite: 1]
            st.markdown("*(Hover over the block below to copy the text)*")
            st.code(translated, language="text")

            # Optional Feature 2: Text-to-Speech[cite: 1]
            st.markdown("### 🔊 Listen to Translation:")
            
            # Generate Audio using Google Text-to-Speech
            tts = gTTS(text=translated, lang=tgt_code, slow=False)
            
            # Save audio to a memory buffer so we don't have to save a file locally
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Play audio in Streamlit
            st.audio(audio_buffer, format='audio/mp3')

        except Exception as e:
            st.error(f"An error occurred during translation: {e}")