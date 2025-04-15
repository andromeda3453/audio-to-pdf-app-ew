# import os
# import shutil
# import streamlit as st
# import sounddevice as sd
# from scipy.io.wavfile import write
# from modules.audio_processor import transcribe_audio
# from modules.nlp_extractor import extract_data
# from modules.template_matcher import match_template
# from modules.word_filler import fill_word_template


# TEMPLATES = {
#     "invoice": {
#         "path": "templates/Fitting Follow-up Generic.pdf",
#         "description": "Invoice for service payment"
#     }
# }

# st.set_page_config(page_title="Mic to PDF", layout="centered")
# st.title("🎤 Speak & Auto-Fill PDF")

# use_mic = st.checkbox("Use microphone instead of uploading audio")

# if use_mic:
#     duration = st.slider("Recording duration (seconds)", 3, 15, 5)
#     if st.button("🎙️ Start Recording"):
#         st.info("Recording...")
#         fs = 16000
#         recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
#         sd.wait()
#         os.makedirs("temp_audio", exist_ok=True)
#         audio_path = "temp_audio/mic_input.wav"
#         write(audio_path, fs, recording)
#         st.success("Recording complete.")
# else:
#     uploaded_audio = st.file_uploader("Upload audio file (MP3/WAV)", type=["mp3", "wav"])
#     if uploaded_audio:
#         audio_path = f"temp_audio/{uploaded_audio.name}"
#         os.makedirs("temp_audio", exist_ok=True)
#         with open(audio_path, "wb") as f:
#             f.write(uploaded_audio.read())
#         st.success("Audio uploaded.")

# # Run pipeline only if audio_path exists
# if "audio_path" in locals():
#     transcript = transcribe_audio(audio_path)
#     st.text_area("🧠 Transcript", transcript, height=150)

#     extracted = extract_data(transcript)
#     st.write("📌 Extracted Data:", extracted)

#     matched_template = match_template(transcript, TEMPLATES)
#     template_path = TEMPLATES[matched_template]["path"]
#     base_name = os.path.splitext(os.path.basename(audio_path))[0]
#     output_path = f"output/filled_{base_name}.pdf"
#     os.makedirs("output", exist_ok=True)
#     fill_pdf(template_path, output_path, extracted)

#     with open(output_path, "rb") as f:
#         st.download_button("📥 Download Filled PDF", f, file_name=f"filled_{base_name}.pdf")

#     shutil.rmtree("temp_audio")

import os
import shutil
import streamlit as st
from scipy.io.wavfile import write
from modules.audio_processor import transcribe_audio
from modules.nlp_extractor import extract_data
from modules.template_matcher import match_template
from modules.word_filler import fill_word_template  # <-- changed from pdf_filler

TEMPLATES = {
    "fitting_followup": {
        "path": "templates/fitting_followup_template.docx",
        "description": "Fitting Follow-up Form"
    }
}

st.set_page_config(page_title="Mic to Word", layout="centered")
st.title("🎤 Speak & Auto-Fill Word Document")


audio_path = None
use_mic = None

if not os.environ.get("STREAMLIT_CLOUD"):
    use_mic = st.checkbox("Use microphone instead of uploading audio")
    import sounddevice as sd
if use_mic:
    duration = st.slider("Recording duration (seconds)", 3, 15, 5)
    if st.button("🎙️ Start Recording"):
        st.info("Recording...")
        fs = 16000
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        os.makedirs("temp_audio", exist_ok=True)
        audio_path = "temp_audio/mic_input.wav"
        write(audio_path, fs, recording)
        st.success("Recording complete.")
else:
    uploaded_audio = st.file_uploader("Upload audio file (MP3/WAV)", type=["mp3", "wav"])
    if uploaded_audio:
        audio_path = f"temp_audio/{uploaded_audio.name}"
        os.makedirs("temp_audio", exist_ok=True)
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.read())
        st.success("Audio uploaded.")

# Run pipeline only if audio_path is available
if audio_path:
    transcript = transcribe_audio(audio_path)
    st.text_area("🧠 Transcript", transcript, height=150)

    extracted, checkboxes = extract_data(transcript)
    st.write("📌 Extracted Data:", extracted)
    st.write("📌 Checkbox Data:", checkboxes)

    matched_template = match_template(transcript, TEMPLATES)
    template_path = TEMPLATES[matched_template]["path"]
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = f"output/filled_{base_name}.docx"
    os.makedirs("output", exist_ok=True)

    data_to_fill = {**extracted, **checkboxes}
    fill_word_template(template_path, output_path, data_to_fill)

    with open(output_path, "rb") as f:
        st.download_button("📥 Download Filled Word Document", f, file_name=f"filled_{base_name}.docx")

    shutil.rmtree("temp_audio")
