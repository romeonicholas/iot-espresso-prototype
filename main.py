import phew
import phew.server
import phew.dns

import secrets

ACCESS_POINT_NAME = "IoT Espresso Assistant"
ACCESS_POINT_DOMAIN = "iot.espresso.net"

# TODO: connect to wifi after setup
# setup.connect_to_wifi(secrets.SSID, secrets.PASSWORD)

def setup_mode():
    print("Entering setup mode...")

    @phew.server.route("/", methods=['GET'])
    def index():
        return "Hello, World!", 200

    @phew.server.route("/wrong-host-redirect", methods=['GET'])
    def wrong_host():
        body = "<!DOCTYPE html><head><meta http-equiv='refresh' content='0;URL=http://" + ACCESS_POINT_DOMAIN + "' /></head>"
        return body

    @phew.server.route("/hotspot-detect.html", methods=["GET"])
    def hotspot():
        return "This is the portal", 200

    @phew.server.catchall()
    def catch_all(request):
        if request.headers.get("host") != ACCESS_POINT_DOMAIN:
            return phew.server.redirect("http://" + ACCESS_POINT_DOMAIN + "/wrong-host-redirect")
        return None

    ap = phew.access_point(ACCESS_POINT_NAME)
    ip = ap.ifconfig()[0]
    phew.dns.run_catchall(ip)


setup_mode()
phew.server.run()
