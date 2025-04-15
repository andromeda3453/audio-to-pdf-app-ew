import os
from faster_whisper import WhisperModel

# 'base' can be changed to 'small', 'medium', etc.
whisper_model = WhisperModel("base")

def transcribe_audio(audio_path: str) -> str:
    """
    Takes the path to an audio file, transcribes it using faster-whisper,
    and returns the transcript as a single string.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    segments, _ = whisper_model.transcribe(audio_path)
    transcript = " ".join(segment.text for segment in segments)
    return transcript
