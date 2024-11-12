import network
import utime

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    connection_attempt = 1

    while not wlan.isconnected() and connection_attempt < 10:
        print("Attempting to connect to wifi: ", connection_attempt)
        connection_attempt += 1
        utime.sleep(5)

    if wlan.isconnected():
        print("Successfully connected to wifi")
    else:
        print("Could not connect to wifi")
