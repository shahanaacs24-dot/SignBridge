from speech.speech_to_text import SpeechToText


stt = SpeechToText()

print("\nSpeak something...")

text = stt.listen()

print("\nRecognized text:")
print(text)