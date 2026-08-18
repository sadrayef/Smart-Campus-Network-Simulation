# ===== Data Center Disaster Recovery Controller (MCU) =====
from gpio import *
from time import *

# ---------- MCU pin map ----------
TEMP_PIN = A0
SMOKE_PIN = A1
LED_RED = 0
LED_GREEN = 1
ALARM = 2
FAN = 3
DOOR = 4
DISPLAY = 5

# ---------- thresholds (real units) ----------
TEMP_C_THRESHOLD = 45.0
SMOKE_THRESHOLD = 10.0

def read_temp_c():
    raw = analogRead(TEMP_PIN)
    c = (raw / 1023.0) * 200.0 - 100.0
    return raw, c

def read_smoke_pct():
    raw = analogRead(SMOKE_PIN)
    # raw = 120
    pct = (raw / 1023.0) * 100.0
    return raw, pct

def setup():
    pinMode(LED_RED, OUT)
    pinMode(LED_GREEN, OUT)
    pinMode(ALARM, OUT)
    pinMode(FAN, OUT)
    pinMode(DOOR, OUT)

def set_normal():
    digitalWrite(LED_GREEN, HIGH)
    digitalWrite(LED_RED, LOW)
    digitalWrite(ALARM, LOW)
    digitalWrite(FAN, LOW)
    digitalWrite(DOOR, LOW)
    customWrite(DISPLAY, "STATUS: NORMAL")

def set_critical():
    digitalWrite(LED_RED, HIGH)
    digitalWrite(LED_GREEN, LOW)
    digitalWrite(ALARM, HIGH)
    digitalWrite(FAN, HIGH)
    digitalWrite(DOOR, HIGH)
    customWrite(DISPLAY, "WARNING! FIRE - EVACUATE")

state = "normal"
setup()
set_normal()
print("Data Center Disaster Recovery - controller started")
print("Monitoring temperature and smoke...")

while True:
    t_raw, t_c = read_temp_c()
    s_raw, s_pct = read_smoke_pct()
    hot = (t_c >= TEMP_C_THRESHOLD)
    smoky = (s_pct >= SMOKE_THRESHOLD)
    print("temp=" + str(round(t_c, 1)) + "C (raw=" + str(t_raw) + ")  smoke=" + str(round(s_pct, 1)) + "% (raw=" + str(s_raw) + ")")
    if hot and smoky:
        if state != "critical":
            state = "critical"
            set_critical()
            print("!!! EMERGENCY: HIGH TEMP + SMOKE detected !!!")
            print("Actions -> Alarm ON, Red LED ON, Fan ON, Door OPEN")
    else:
        if state != "normal":
            state = "normal"
            set_normal()
            print("Recovered -> conditions normal. Systems restored (Green LED).")
    sleep(1)


