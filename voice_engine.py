"""
voice_engine.py - Regional Voice Synthesis Engine
Provides voice-first audio playback in Hindi, Tamil, and English for Tier-2/3 investors.
"""
import os
import tempfile
from gtts import gTTS

LANG_MAP = {
    "हिन्दी (Hindi)": "hi",
    "தமிழ் (Tamil)": "ta",
    "English": "en"
}

def generate_regional_audio(text: str, language_name: str) -> str:
    """Generates an .mp3 audio file from text in the selected Indian language."""
    if not text:
        return None
        
    lang_code = LANG_MAP.get(language_name, "hi")
    
    try:
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "scam_satark_voice.mp3")
        
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Voice generation warning: {e}")
        return None
