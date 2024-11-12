from phew import server, access_point, dns
from phew.template import render_template

import secrets

ACCESS_POINT_NAME = "IoT Espresso Assistant"
ACCESS_POINT_DOMAIN = "iot.espresso.net"

# TODO: connect to wifi after setup
# setup.connect_to_wifi(secrets.SSID, secrets.PASSWORD)

def setup_mode():
    print("Entering setup mode...")

    @server.route("/", methods=['GET'])
    def index(request):
        if request.headers.get("host").lower() != ACCESS_POINT_DOMAIN:
            return render_template("templates/redirect.html", domain = ACCESS_POINT_DOMAIN)

        return render_template("templates/index.html")

    
    @server.catchall()
    def catch_all(request):
        if request.headers.get("host") != ACCESS_POINT_DOMAIN:
            return render_template("templates/redirect.html", domain=ACCESS_POINT_DOMAIN)

        return "Not found", 404

    ap = access_point(ACCESS_POINT_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)


setup_mode()
server.run()
