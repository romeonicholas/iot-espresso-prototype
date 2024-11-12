from machine import Pin
from utime import sleep
import network
import urequests

import secrets

pin = Pin("LED", Pin.OUT)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)

cat_fact_req = urequests.get("http://cat-fact.herokuapp.com/facts")
cat_fact = cat_fact_req.json()
print(cat_fact)

print("LED starts flashing...")
while True:
    try:
        pin.toggle()
        sleep(1)  # sleep 1sec
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")
