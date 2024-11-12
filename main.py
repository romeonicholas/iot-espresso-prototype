from phew import server, access_point, dns

import secrets

ACCESS_POINT_NAME = "IoT Espresso Assistant"
ACCESS_POINT_DOMAIN = "iot.espresso.net"

# TODO: connect to wifi after setup
# setup.connect_to_wifi(secrets.SSID, secrets.PASSWORD)

def setup_mode():
    print("Entering setup mode...")

    @server.route("/", methods=['GET'])
    def index(request):
        return "Hello, World!", 200

    @server.route("/wrong-host-redirect", methods=['GET'])
    def wrong_host(request):
        body = "<!DOCTYPE html><head><meta http-equiv='refresh' content='0;URL=http://" + ACCESS_POINT_DOMAIN + "' /></head>"
        return body

    @server.route("/hotspot-detect.html", methods=["GET"])
    def hotspot(request):
        return "This is the portal", 200

    @server.catchall()
    def catch_all(request):
        if request.headers.get("host") != ACCESS_POINT_DOMAIN:
            return server.redirect("http://" + ACCESS_POINT_DOMAIN + "/wrong-host-redirect")
        return None

    ap = access_point(ACCESS_POINT_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)


setup_mode()
server.run()
