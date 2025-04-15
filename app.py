from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import uuid
import shutil
import sounddevice as sd
from scipy.io.wavfile import write
from modules.audio_processor import transcribe_audio
from modules.nlp_extractor import extract_data
from modules.template_matcher import match_template
from modules.pdf_filler import fill_pdf
import spacy.cli

spacy.cli.download("en_core_web_sm")

app = Flask(__name__, template_folder='template')

TEMPLATES = {
    "invoice": {
        "path": "templates/sample_fillable_form.pdf",
        "description": "Invoice for service payment"
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'use_mic' in request.form:
            duration = int(request.form.get('duration', 5))
            fs = 16000
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            os.makedirs("temp_audio", exist_ok=True)
            audio_path = "temp_audio/mic_input.wav"
            write(audio_path, fs, recording)
        elif 'audio_file' in request.files:
            audio = request.files['audio_file']
            if audio.filename == '':
                return "No selected file", 400
            os.makedirs("temp_audio", exist_ok=True)
            audio_path = f"temp_audio/{uuid.uuid4()}.mp3"
            audio.save(audio_path)
        else:
            return "No input provided", 400

        transcript = transcribe_audio(audio_path)
        extracted = extract_data(transcript)
        matched_template = match_template(transcript, TEMPLATES)
        template_path = TEMPLATES[matched_template]["path"]
        os.makedirs("output", exist_ok=True)
        output_path = f"output/filled_{uuid.uuid4()}.pdf"
        fill_pdf(template_path, output_path, extracted)

        shutil.rmtree("temp_audio")
        return send_file(output_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
