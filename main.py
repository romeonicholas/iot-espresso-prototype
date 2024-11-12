import machine
import utime
import urequests

import setup
import secrets

pin = machine.Pin("LED", machine.Pin.OUT)

setup.connect_to_wifi(secrets.SSID, secrets.PASSWORD)

cat_fact_req = urequests.get("http://cat-fact.herokuapp.com/facts")
cat_fact = cat_fact_req.json()
print(cat_fact)

print("LED starts flashing...")
while True:
    try:
        pin.toggle()
        utime.sleep(1)  # sleep 1sec
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")
