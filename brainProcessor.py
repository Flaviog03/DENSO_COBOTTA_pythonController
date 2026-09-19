import os
import json
from AI.ai_transformer import AITransformer, AITransformerError
from AI import ai_utilities
from dotenv import load_dotenv
from densoController import DirectionMap, RobotAction

class BrainProcessor:
    def __init__(self, actions, directions, responseSchemaName):
        # L'inizializzazione legge automaticamente le variabili d'ambiente[cite: 1]
        try:
            self.ai = AITransformer()
        except AITransformerError as e:
            print(f"Inizializzazione fallita: {e}")
            raise
            
        # Carichiamo lo schema strutturato dalla cartella schemas/
        self.schema = ai_utilities.getSchema(responseSchemaName)

        # Inietto le azioni e le direzioni nello schema
        self.schema["properties"]["comando"]["enum"] = actions
        self.schema["properties"]["direzione"]["enum"] = directions

        # Il System Prompt che istruisce il modello sulle azioni consentite
        self.system_prompt = f"""
                Sei il traduttore logico di un braccio robotico DENSO.
                Il tuo unico scopo è estrarre comandi operativi da frasi in italiano e convertirli IN UN FORMATO ESCLUSIVAMENTE JSON. 
                NON SCRIVERE NESSUNA PAROLA O SPIEGAZIONE FUORI DAL JSON.

                AZIONI CONSENTITE: {actions}.
                DIREZIONI CONSENTITE (solo per l'azione TRANSLATE): {directions}.

                REGOLE FISSE:
                1. Se l'utente chiede di spostarsi, usa "TRANSLATE" e specifica la "direzione".
                2. Se non viene indicata una distanza esatta, usa sempre "valore_mm": 50. Se specificata, inserisci il numero.
                3. Se l'utente chiede di prendere, pinzare o afferrare, usa "GRAB" (senza direzione e senza valore_mm).
                4. Se l'utente chiede di mollare, lasciare o aprire, usa "RELEASE".

                ESEMPI DI RISPOSTA:
                Input: "vai in avanti di 100 millimetri"
                Output: {"azione": "TRANSLATE", "direzione": "avanti", "valore_mm": 100}

                Input: "spostati un po' a destra"
                Output: {"azione": "TRANSLATE", "direzione": "destra", "valore_mm": 50}

                Input: "chiudi la pinza e prendi il peluche"
                Output: {"azione": "GRAB"}

                Input: "lascia andare"
                Output: {"azione": "RELEASE"}
            """

    def process_command(self, user_text: str) -> dict | None:
        print(f"Analisi del comando: '{user_text}'...")

        if self.ai.modello is None:
            raise AITransformerError("Il modello Ai non è stato caricato correttamente")
        
        # Generiamo il dizionario payload formattato con i ruoli system e user
        payload = ai_utilities.getPayload(
            prompt=self.system_prompt,
            responseSchema=self.schema,
            params=user_text,
            model=self.ai.modello,
            schemaName="conversioneTestuale"
        )
        
        try:
            # Inviamo la request HTTP a LM Studio
            risposta = self.ai.askAI(payload=json.dumps(payload))
            
            # Poiché LM Studio restituisce un JSON in formato OpenAI-compatibile,
            # il contenuto vero e proprio si trova dentro la lista 'choices'
            raw_content = risposta['choices'][0]['message']['content']
            
            # Il contenuto è una stringa in formato JSON, va convertito in dizionario Python
            json_data = json.loads(raw_content)
            return json_data
            
        except AITransformerError as e:
            print(f"Errore di connessione o URL mancante: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Errore nella decodifica della risposta di LM Studio: {e}")
            return None

if __name__ == "__main__":
    load_dotenv()
    cervello = BrainProcessor(actions=RobotAction.get_allowed_actions(), directions=DirectionMap.get_allowed_directions(), responseSchemaName="Prova")