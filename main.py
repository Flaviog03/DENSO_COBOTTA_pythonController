from voiceRecognition import VoiceProcessor

if __name__ == "__main__":
    orecchio = VoiceProcessor()
    comando = orecchio.listen_and_transcribe()
    print(f"Trascrizione: {comando}")