# ========================
# MODEL AYARLARI
# ========================

MODEL_PATH = "yolov8n.pt"
CONF_THRESHOLD = 0.75   # artırıldı

# ========================
# PID AYARLARI
# ========================

KP = 0.12
KI = 0.0
KD = 0.04

# ========================
# PWM AYARLARI
# ========================

PWM_MIN = 1350
PWM_MAX = 1650
PWM_NEUTRAL = 1500

# ========================
# KONTROL SINIRLARI
# ========================

MAX_CONTROL = 1
LOST_TIMEOUT = 0.5
JITTER_THRESHOLD = 5

# ========================
# TRACKER AYARLARI
# ========================

MAX_DISTANCE = 25
MAX_MISSING = 10