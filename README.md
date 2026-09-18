# 1. Inizializzazione
        # 1.1 Connessione al robot
        # 1.2 Forza velocità del robot al 40%
        # 1.3 Inizializza "orecchio virtuale"

# 2. Corpo del programma (Ciclo)
    # 2.1 Acquisizione input
        # 2.1.1 Acquisizione posizione attuale -> lista [x,y,z,Rx,Ry,Rz]
        # 2.1.2 Impostazione del filtro silero-vad per voce chiara
        # 2.1.3 Acquisizione comando vocale (richiede una mappatura dei comandi) -> frasi in linguaggio naturale

    # 2.2 Comunicazione con l'AI
        # 2.2.1 Classificazione dei possibili comandi (traslazione/rotazione/afferra/rilascia)
        # 2.2.2 Breve check (se contiene afferra verifica che la pinza non sia già chiusa)
        # 2.2.3 Invio dei comandi in linguaggio naturale codificati all'interno di un file con formato JSON
        # 2.2.4 -!- Comunicazione con il modello (effettuerà la classificazione dell'input) 
            -> file JSON
        # 2.2.5 Validazione formato file JSON
        # 2.2.6 Calcolo nuova posizione
        # 2.2.7 Verifica fattibilità movimento tramite coordinate attuali (es. fuoriRange, fuoriBoxSicurezza)
        # Esecuzione

    # 2.3 Movimentazione del braccio 
        # -!- I movimenti avverranno secondo delle unità base, es (50 mm alla volta)

# 3. Operazioni finali e Rilascio connessione
