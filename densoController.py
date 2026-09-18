from pybcapclient.bcapclient import BCAPClient
import time
from enum import IntEnum, StrEnum

class DirectionMap(StrEnum):
    """
    Il primo elemento è un numero ed è l'indice dell'asse all'interno del vettore delle coordinate
    Il secondo elemento è il  che indica il verso del vettore individuato da uno dei tre assi
    """
    FORWARD  = "0,+1"
    BACKWARD = "0,-1"
    RIGHT    = "1,-1"
    LEFT     = "1,+1"
    UP       = "2,+1"
    DOWN     = "2,-1"

    @classmethod
    def get_allowed_directions(cls) -> list[str]:
        """Restituisce le direzioni consentite leggendole dinamicamente dall'Enum"""
        return [direction.name for direction in cls]
    

class RobotAction(IntEnum):
    TRANSLATE = 0
    ROTATE = 1
    GRAB = 2
    RELEASE = 3

    @classmethod
    def get_allowed_actions(cls) -> list[str]:
        """Restituisce le azioni consentite leggendole dinamicamente dall'Enum"""
        return [action.name for action in cls]

class DensoController:
    def __init__(self, ip_address="192.168.0.1", port=5007, timeout=2000):
        self.ip = ip_address
        self.port = port

        # Inizializza il client: l'apertura del socket avviene automaticamente qui (timeout 2000 ms)
        self.bcap = BCAPClient(self.ip, self.port, timeout) 
        print("Connessione aperta")

        self.bcap.service_start("")
        print("Servizio b-CAP avviato")

        self.h_ctrl = None
        self.h_rob = None
        self.CurPosHandl = None

    def connect(self):
        # Connessione al controller virtuale o reale
        Name = ""
        Provider = "CaoProv.DENSO.VRC"   # usa "CaoProv.DENSO.VRC9" per un RC9
        Machine = "localhost"
        Option = ""
        self.h_ctrl = self.bcap.controller_connect(Name, Provider, Machine, Option)
        print("Connesso al controller, handle:", self.h_ctrl)

        # --- Handle dell'oggetto Robot ---
        self.h_rob = self.bcap.controller_getrobot(self.h_ctrl, "Arm", "")
        print("Handle Robot ottenuto:", self.h_rob)

        # --- Presa di controllo del braccio ---
        self.bcap.robot_execute(self.h_rob, "TakeArm", [0, 0])
        print("TakeArm eseguito")

        # --- Accensione motori ---
        self.bcap.robot_execute(self.h_rob, "Motor", [1, 0])
        print("Motori ON")

        # --- Velocità/accelerazione/decelerazione esterne (%) - bassa per sicurezza ---
        self.bcap.robot_execute(self.h_rob, "ExtSpeed", [40, 100, 100])
        print("Velocità impostata al 20%")

    def setSpeedAccDec(self, speed : int, acc=100, dec=100):
        """ Imposta la velocità/accelerazione/decelerazione del robot """
        self.bcap.robot_execute(self.h_rob, "ExtSpeed", [speed, acc, dec])
        print(f"Velocità impostata al {speed}%")

    def getActualPosition(self) -> list:
        """ Restituisce le coordinate attuali del robot """
        CurPosHandl = self.bcap.robot_getvariable(self.h_rob, "@CURRENT_POSITION", "")
        pos_iniziale = self.bcap.variable_getvalue(CurPosHandl)
        return pos_iniziale

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
        # --- Spegnimento motori ---
        self.bcap.robot_execute(self.h_rob, "Motor", [0, 0])
        print("Motori OFF")

        if self.CurPosHandl:
            self.bcap.variable_release(self.CurPosHandl)
        if self.h_rob:
            self.bcap.robot_execute(self.h_rob, "GiveArm", None)
            self.bcap.robot_release(self.h_rob)
            print("GiveArm eseguito e Robot rilasciato")
        if self.h_ctrl:
            self.bcap.controller_disconnect(self.h_ctrl)
            print("Controller disconnesso")
        self.bcap.service_stop()
        print("Servizio b-CAP fermato")

# ==========================================
# ESECUZIONE DEL TEST
# ==========================================
if __name__ == "__main__":
    robot = DensoController(ip_address="172.20.10.2") # L'IP della tua VM Windows
    
    try:
        robot.connect()
    
        # 2. Comando effettivo di spostamento alla variabile
        robot.esegui_presa("P1")
        
    except Exception as e:
        print(f"Errore b-CAP: {e}")
    finally:
        robot.disconnect()