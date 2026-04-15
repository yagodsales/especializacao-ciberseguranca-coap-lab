from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
import datetime

class TimeResource(Resource):
    def __init__(self, name="TimeResource", coap_server=None):
        super(TimeResource, self).__init__(name, coap_server, visible=True,
                                           observable=True, allow_children=True)
        self.payload = "init"

    def render_GET(self, request):
        self.payload = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self

class HealthResource(Resource):
    def __init__(self, name="HealthResource", coap_server=None):
        super(HealthResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=False)
        self.payload = "ok"

    def render_GET(self, request):
        return self

class CoAPServer(CoAP):
    def __init__(self, host, port):
        super(CoAPServer, self).__init__((host, port))
        self.add_resource("time/", TimeResource())
        self.add_resource("health/", HealthResource())

def main():
    server = CoAPServer("0.0.0.0", 5683)
    print("CoAP server running on 0.0.0.0:5683")
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server shutdown")
        server.close()

if __name__ == "__main__":
    main()