import streamlit as st
import speech_recognition as sr
import pyttsx3

try:
    engine = pyttsx3.init()
except Exception as e:
    engine = None
    print(f"Failed to initialize Text-to-Speech engine: {e}")


def recognize_speech_live():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎙️ Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=45)
            text = recognizer.recognize_google(audio)
            st.success(f"🗣️ You said: {text}")
            return text
    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand your response.")
    except sr.RequestError:
        st.error("⚠️ Speech recognition service unavailable.")
    except Exception as e:
        st.error(f"❌ Microphone Error: {str(e)}")
    return ""


def speak(text):
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            st.error(f"TTS Error: {e}")