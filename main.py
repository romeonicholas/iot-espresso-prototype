import os
import json

import phew
from setup_mode import setup_mode
from app_mode import app_mode

CONFIG_FILE = "config.json"
WIFI_MAX_ATTEMPTS = 3


try:
    print("Checking for config file...")
    os.stat(CONFIG_FILE)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        wifi_credentials = json.load(f)

    for attempt in range(WIFI_MAX_ATTEMPTS):
        ip_address = phew.connect_to_wifi(
            wifi_credentials["ssid"], wifi_credentials["password"]
        )

        if phew.is_connected_to_wifi():
            print(f"Connected to wifi with IP address: {ip_address}")
            break
        else:
            print(f"Failed attempt to connect to wifi: {attempt + 1}")

    if phew.is_connected_to_wifi():
        app_mode()
    else:
        os.remove(CONFIG_FILE)
        setup_mode()

except Exception as e:
    print(e)
    setup_mode()
