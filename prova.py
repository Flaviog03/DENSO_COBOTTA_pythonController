import pybcapclient.bcapclient as bcapclient

# --- Parametri di connessione ---
host = "127.0.0.1"   # localhost: la simulazione VRC gira sullo stesso PC
port = 5007           # porta di default del server b-CAP (NON quella OPC-UA)
timeout = 2000

m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Connessione aperta")

m_bcapclient.service_start("")
print("Servizio b-CAP avviato")

Name = ""
Provider = "CaoProv.DENSO.VRC"   # usa "CaoProv.DENSO.VRC9" per un RC9
Machine = "localhost"
Option = ""

hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connesso al controller, handle:", hCtrl)

HRobot = None
CurPosHandl = None

try:
    # --- Handle dell'oggetto Robot ---
    HRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
    print("Handle Robot ottenuto:", HRobot)

    # --- Presa di controllo del braccio ---
    m_bcapclient.robot_execute(HRobot, "TakeArm", [0, 0])
    print("TakeArm eseguito")

    # --- Accensione motori ---
    m_bcapclient.robot_execute(HRobot, "Motor", [1, 0])
    print("Motori ON")

    # --- Velocità/accelerazione/decelerazione esterne (%) - bassa per sicurezza ---
    m_bcapclient.robot_execute(HRobot, "ExtSpeed", [20, 100, 100])
    print("Velocità impostata al 20%")

    # --- Lettura posizione attuale [x, y, z, rx, ry, rz, fig] ---
    CurPosHandl = m_bcapclient.robot_getvariable(HRobot, "@CURRENT_POSITION", "")
    pos_iniziale = m_bcapclient.variable_getvalue(CurPosHandl)
    print("Posizione attuale:", pos_iniziale)

    # --- Calcolo posizione target: +50 mm su Z rispetto alla attuale ---
    pos_target = list(pos_iniziale)
    pos_target[2] += 50.0  # indice 2 = Z

    # --- Movimento verso l'alto (Comp=2 -> interpolazione lineare CP) ---
    Pose = [pos_target, "P", "@E"]
    m_bcapclient.robot_move(HRobot, 2, Pose, "")
    print("Spostato di +50mm su Z")

    # --- Ritorno alla posizione di partenza ---
    Pose = [list(pos_iniziale), "P", "@E"]
    m_bcapclient.robot_move(HRobot, 2, Pose, "")
    print("Tornato alla posizione iniziale")

    # --- Spegnimento motori ---
    m_bcapclient.robot_execute(HRobot, "Motor", [0, 0])
    print("Motori OFF")

finally:
    # --- Rilascio risorse e disconnessione, sempre eseguito ---
    if CurPosHandl:
        m_bcapclient.variable_release(CurPosHandl)
    if HRobot:
        m_bcapclient.robot_execute(HRobot, "GiveArm", None)
        m_bcapclient.robot_release(HRobot)
        print("GiveArm eseguito e Robot rilasciato")
    if hCtrl:
        m_bcapclient.controller_disconnect(hCtrl)
        print("Controller disconnesso")
    m_bcapclient.service_stop()
    print("Servizio b-CAP fermato")