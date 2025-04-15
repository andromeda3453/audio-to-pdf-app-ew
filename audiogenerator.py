from gtts import gTTS

text = """My name is Manuj Agarwal. The date of follow-up is June 3rd, 2025.
Provider number is 4269121J
Patient’s name is John Smith, date of birth is January 1st, 2012, referred by Dr. Thomas
This was a private fitting. HSP has been signed. Targets were met
Education and communication strategies were reviewed
Battery change and cleaning were reviewed
The patient reported comfort with the hearing device
Future recall has been scheduled"""

tts = gTTS(text)
tts.save("sample_audio.mp3")
