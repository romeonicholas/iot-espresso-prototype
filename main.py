import os
import json
import machine
import utime 

from phew import server, access_point, dns
from phew.template import render_template

ACCESS_POINT_NAME = "IoT Espresso Assistant"
ACCESS_POINT_DOMAIN = "iot.espresso.net"
CONFIG_FILE = "config.json"


def setup_mode():
    print("Entering setup mode...")

    @server.route("/", methods=['GET'])
    def index(request):
        if request.headers.get("host").lower() != ACCESS_POINT_DOMAIN:
            return render_template("templates/redirect.html", domain = ACCESS_POINT_DOMAIN)

        return render_template("templates/index.html")

    @server.route("/setup", methods=['POST'])
    def setup(request):
        ssid = request.form.get("ssid")

        if not ssid:
            return "SSID is required", 400

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(request.form, f)
            f.close()

        return render_template("templates/index.html")

    @server.catchall()
    def catch_all(request):
        if request.headers.get("host") != ACCESS_POINT_DOMAIN:
            return render_template("templates/redirect.html", domain=ACCESS_POINT_DOMAIN)

        return "Not found", 404

    ap = access_point(ACCESS_POINT_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)

try:
    os.stat(CONFIG_FILE)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        wifi_credentials = json.load(f)

        print("Trying to connec to network...")
        # TODO: connect to wifi after setup
        # setup.connect_to_wifi(config.SSID, config.PASSWORD)

except Exception:
    print("Couldn't connect to network, entering setup mode...")
    setup_mode()


server.run()
