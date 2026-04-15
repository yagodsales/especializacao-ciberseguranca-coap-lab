import os
import time
from coapthon.client.helperclient import HelperClient

server_host = os.getenv("COAP_SERVER_HOST", "172.28.0.10")
server_port = int(os.getenv("COAP_SERVER_PORT", "5683"))

client = None

try:
    client = HelperClient(server=(server_host, server_port))
    print(f"[INFO] Sending GET /time to {server_host}:{server_port} every 1 second")

    counter = 1
    while True:
        try:
            response = client.get("time")
            if response is not None:
                print(f"[{counter}] Code: {response.code} | Payload: {response.payload}")
            else:
                print(f"[{counter}] Empty response")
        except Exception as e:
            print(f"[{counter}] Error: {e}")

        counter += 1
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[INFO] Client interrupted by user")

finally:
    if client is not None:
        client.stop()