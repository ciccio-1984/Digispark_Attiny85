import machine
import dht
import time

# Configurazione pin e sensore
pinDHT11 = machine.Pin(2)
sensor = dht.DHT11(pinDHT11)

pinLED = machine.Pin(4, machine.Pin.OUT)

# Stato relè
relay_state = 0
pinLED.value(relay_state)

# Tempo minimo di accensione: 30 minuti
MIN_ON_MS = 30 * 60 * 1000

# Momento in cui il relè si è acceso
on_time = 0

def read_dht11():
    global relay_state, on_time

    try:
        sensor.measure()
        humidity = sensor.humidity()
        temperature = sensor.temperature()
        now = time.ticks_ms()

        print('=================================')
        print('Temp:', temperature, 'C  Hum:', humidity, '%')
        print('Relay:', relay_state)

        # --- ACCENSIONE ---
        if humidity >= 60 and relay_state == 0:
            relay_state = 1
            pinLED.value(1)
            on_time = now
            print('Relè ACCESO → parte il timer 30 min')

        # --- SPEGNIMENTO (solo se timer scaduto) ---
        elif humidity <= 55 and relay_state == 1:
            elapsed = time.ticks_diff(now, on_time)

            if elapsed >= MIN_ON_MS:
                relay_state = 0
                pinLED.value(0)
                print('Relè SPENTO (30 min trascorsi)')
            else:
                remaining = (MIN_ON_MS - elapsed) // 60000
                print('Spegnimento BLOCCATO, mancano', remaining, 'min')

    except OSError as e:
        print('Errore lettura DHT11:', e)

# Loop principale
while True:
    read_dht11()
    time.sleep(2)
