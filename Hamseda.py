import openai
import speech_recognition as sr
import langdetect
import pyttsx3
import gtts
import os
import playsound

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_whisper(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None

def detect_language(text):
    try:
        lang = langdetect.detect(text)
        print(f"Detected Language: {lang}")
        return lang
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

def translate_text(text, target_language):
    openai.api_key = "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"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate this text to {target_language}: {text}"},
        ]
    )
    
    translated_text = response["choices"][0]["message"]["content"]
    print(f"Translated: {translated_text}")
    return translated_text

def text_to_speech(text, language):
    tts = gtts.gTTS(text, lang=language)
    filename = "output.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def main():
    while True:
        text = recognize_speech()
        if not text:
            continue
        
        source_language = detect_language(text)
        if not source_language:
            continue
        
        target_language = input("Enter target language (e.g., 'fr' for French, 'es' for Spanish): ")
        translated_text = translate_text(text, target_language)
        text_to_speech(translated_text, target_language)

if __name__ == "__main__":
    main()
