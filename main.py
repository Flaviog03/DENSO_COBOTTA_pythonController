from voiceRecognition import VoiceProcessor
from densoController import RobotAction, DirectionMap
from pybcapclient.bcapclient import BCAPClient
from densoController import DensoController
from AI.ai_transformer import AITransformer, AITransformerError
from AI import ai_utilities
from dotenv import load_dotenv

# Imposta l'IP del COBOTTA reale (di fabbrica è 192.168.0.1)
# Se stai testando su WINCAPS III, usa "172.20.10.2" o "127.0.0.1"[cite: 2, 4]
### PARAMETERS
ROBOT_IP = "192.168.1.15" 
ROBOT_PORT = 5007
TIMEOUT_MS = 2000
SPEED_LIMIT = 40
DBG = 2 # 1:ModuloVoce | 2:ModuloMovimento


if __name__ == "__main__":
    try:
        # 1.1 Connessione al controller
        controller = DensoController(ip_address=ROBOT_IP, port=ROBOT_PORT, timeout=TIMEOUT_MS)
        controller.connect()
        comandoUtente = ""

        # 1.2 Imposto la velocità al 40%
        controller.setSpeedAccDec(SPEED_LIMIT)

        # 1.3 Inizializzazione "orecchio virtuale"
        if DBG != 2:
            orecchio = VoiceProcessor()

        # 1.4 Inizializzazione AITransformer
        load_dotenv()
        transformer = AITransformer()

        # 2 - Corpo principale del programma
        while comandoUtente != "Esci":
            # 2.1 Acquisizione input
            posizioneAttuale = controller.getActualPosition()

            if DBG != 2:
                comandoUtente = orecchio.listen_and_transcribe()
            else:
                # Faccio un mock 
                comandoUtente = "trasla il braccio in avanti"

            azioniConsentite = RobotAction.get_allowed_actions()
            direzioniConsentite = DirectionMap.get_allowed_directions()

            prompt = 

            

            break


    except Exception as e:
        print(e)
    finally:
        controller.disconnect()


"""
IDEE: Salva la posizione del robot tramite comando vocale
"""

     



