# Installazione: pip install faster-whisper SpeechRecognition PyAudio
import speech_recognition as sr
from faster_whisper import WhisperModel
import os

class VoiceProcessorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class VoiceProcessor:
    def __init__(self, model_size="turbo"):
        print("Caricamento del modello AI vocale...")
        # Cambia 'cpu' in 'cuda' se configuri una GPU Nvidia su Windows
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.recognizer = sr.Recognizer()

    def listen_and_transcribe(self):
        with sr.Microphone() as source:
            print("Calibrazione rumore di fondo... attendi 1 secondo.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("In ascolto! Parla ora...")
            audio = self.recognizer.listen(source)

        # Salvataggio temporaneo per garantire compatibilità con Whisper
        temp_file = "temp_cmd.wav"
        with open(temp_file, "wb") as f:
            f.write(audio.get_wav_data())

        print("Trascrizione in corso...")
        segments, _ = self.model.transcribe(temp_file, language="it", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
        testo = " ".join([segment.text for segment in segments]).strip()
        
        # Pulizia del file temporaneo
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        return testo