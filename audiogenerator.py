from gtts import gTTS

text = "My name is John. The date is April 10th, 2025. This is for an invoice."
tts = gTTS(text)
tts.save("sample_audio.mp3")
