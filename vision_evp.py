from pybcapclient.bcapclient import BCAPClient
import time

class DensoController:
    def __init__(self, ip_address="172.20.10.2", port=5007):
        self.ip = ip_address
        self.port = port
        # Inizializza il client: l'apertura del socket avviene automaticamente qui (timeout 2000 ms)[cite: 1]
        self.bcap = BCAPClient(self.ip, self.port, 2000) 
        self.h_ctrl = 0
        self.h_rob = 0

    def connect(self):
        # Connessione al controller virtuale o reale[cite: 1]
        self.h_ctrl = self.bcap.controller_connect("", "CaoProv.DENSO.VRC", self.ip, "")
        self.h_rob = self.bcap.controller_getrobot(self.h_ctrl, "Arm", "")
        
        # Acquisizione permessi e accensione motori usando i metodi snake_case[cite: 1]
        self.bcap.robot_execute(self.h_rob, "TakeArm", [0, 1])
        self.bcap.robot_execute(self.h_rob, "Motor", [1, 0])
        print("Motori attivati. Braccio pronto.")

    def mock_evp_vision(self, target_variable="P1"):
        """
        Simula il lavoro che farà il DENSO EVP.
        Invece di usare una telecamera, iniettiamo noi delle coordinate fittizie.
        Formato DENSO: [X, Y, Z, Rx, Ry, Rz, Fig]
        """
        print(f"Simulazione EVP: Calcolo coordinate fittizie del blocco...")
        
        # Coordinate fittizie (es. un blocco sul tavolo a X=250, Y=100, Z=50)
        mock_coords = [250.0, 100.0, 50.0, 180.0, 0.0, 180.0, 5]
        
        # 1. Recupero handle della variabile di posizione (es. P1) dal controller[cite: 1]
        h_pos_var = self.bcap.controller_getvariable(self.h_ctrl, target_variable, "")
        
        # 2. Scrittura delle coordinate fittizie dentro P1[cite: 1]
        self.bcap.variable_putvalue(h_pos_var, mock_coords)
        
        # 3. Rilascio sicuro dell'oggetto variabile in memoria[cite: 1]
        self.bcap.variable_release(h_pos_var)
        
        print(f"Coordinate scritte con successo in {target_variable}: {mock_coords}")

    def esegui_presa(self, target_variable="P1"):
        """
        Comanda al robot di spostarsi sulla variabile calcolata dalla visione.
        """
        print(f"Inizio traiettoria verso {target_variable}...")
        
        movimento = f"@E {target_variable}"
        self.bcap.robot_execute(self.h_rob, "Move", [1, movimento])
        
        print("Posizione raggiunta! (Simulazione chiusura pinza in corso...)")
        time.sleep(1) 

    def disconnect(self):
        # Rilascio risorse con sintassi Pythonic della libreria[cite: 1]
        if self.h_rob:
            self.bcap.robot_execute(self.h_rob, "Motor", [0, 0])
            self.bcap.robot_execute(self.h_rob, "GiveArm", "")
            self.bcap.robot_release(self.h_rob)
        if self.h_ctrl:
            self.bcap.controller_disconnect(self.h_ctrl)
            
        # Niente self.bcap.bCap_Close() perché il socket viene 
        # disconnesso nel __del__ nativo dell'oggetto BCAPClient[cite: 1].
        print("Disconnesso in sicurezza dal controller DENSO.")

# ==========================================
# ESECUZIONE DEL TEST
# ==========================================
if __name__ == "__main__":
    robot = DensoController(ip_address="172.20.10.2") # L'IP della tua VM Windows
    
    try:
        robot.connect()
        # 1. Simula l'elaborazione EVP iniettando le coordinate
        robot.mock_evp_vision("P1")
        
        # 2. Comando effettivo di spostamento alla variabile
        robot.esegui_presa("P1")
        
    except Exception as e:
        print(f"Errore b-CAP: {e}")
    finally:
        robot.disconnect()