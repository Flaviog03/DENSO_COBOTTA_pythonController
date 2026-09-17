from voiceRecognition import VoiceProcessor
from pybcapclient.bcapclient import BCAPClient

# Imposta l'IP del COBOTTA reale (di fabbrica è 192.168.0.1)
# Se stai testando su WINCAPS III, usa "172.20.10.2" o "127.0.0.1"[cite: 2, 4]
ROBOT_IP = "192.168.0.1" 
ROBOT_PORT = 5007
TIMEOUT_MS = 2000

def test_connessione():
    print(f"Tentativo di connessione a {ROBOT_IP}:{ROBOT_PORT}...")
    
    try:
        bcap = BCAPClient(ROBOT_IP, ROBOT_PORT, TIMEOUT_MS)
        
        # CORREZIONE: Il parametro 'machine' (terzo) deve essere vuoto ("") 
        # perché il b-CAP server è già in esecuzione sul controller fisico.
        h_ctrl = bcap.controller_connect("", "CaoProv.DENSO.RC8", "", "")
        
        print(f"✅ Connessione TCP stabilita e servizio b-CAP operativo!")
        print(f"-> Handle del controller assegnato: {h_ctrl}")
        
        bcap.controller_disconnect(h_ctrl)
        print("Disconnessione dal controller completata in sicurezza.")
        
    except Exception as e:
        print(f"❌ Errore b-CAP o di sistema: {e}")

if __name__ == "__main__":
    test_connessione()

"""
if __name__ == "__main__":
    orecchio = VoiceProcessor()
    comando = orecchio.listen_and_transcribe()
    print(f"Trascrizione: {comando}")

    """