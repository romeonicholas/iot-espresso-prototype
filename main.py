import os
import json
import machine
import utime
import urequests
import _thread

from phew import (
    server,
    access_point,
    dns,
    connect_to_wifi,
    is_connected_to_wifi,
    is_connected_to_wifi,
)
from phew.template import render_template

ACCESS_POINT_NAME = "IoT Espresso Assistant"
ACCESS_POINT_DOMAIN = "iot.espresso.net"
CONFIG_FILE = "config.json"
WIFI_MAX_ATTEMPTS = 3


def machine_reset():
    utime.sleep(1)
    machine.reset()


def setup_mode():
    @server.route("/", methods=["GET"])
    def index(request):
        if request.headers.get("host").lower() != ACCESS_POINT_DOMAIN:
            return render_template(
                "templates/redirect.html", domain=ACCESS_POINT_DOMAIN
            )

        return render_template("templates/index.html")

    @server.route("/setup", methods=["POST"])
    def setup(request):
        ssid = request.form.get("ssid")

        if not ssid:
            return "SSID is required", 400

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(request.form, f)
            f.close()

        _thread.start_new_thread(machine_reset, ())
        return render_template("updated.html", access_point_ssid=ACCESS_POINT_NAME)

    @server.catchall()
    def catch_all(request):
        if request.headers.get("host") != ACCESS_POINT_DOMAIN:
            return render_template(
                "templates/redirect.html", domain=ACCESS_POINT_DOMAIN
            )

        return "Not found", 404

    ap = access_point(ACCESS_POINT_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)
    server.run()


def application_mode():
    print("Entering application mode...")
    return None


try:
    os.stat(CONFIG_FILE)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        wifi_current_attempt = 1
        wifi_credentials = json.load(f)

        while wifi_current_attempt <= WIFI_MAX_ATTEMPTS:
            ip_address = connect_to_wifi(
                wifi_credentials["ssid"], wifi_credentials["password"]
            )

            if is_connected_to_wifi():
                wifi_current_attempt = WIFI_MAX_ATTEMPTS + 1
            else:
                wifi_current_attempt += 1

        if is_connected_to_wifi():
            application_mode()
        else:
            os.remove(CONFIG_FILE)
            setup_mode()

except Exception as e:
    print(e)
    setup_mode()
