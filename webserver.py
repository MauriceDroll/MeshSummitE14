import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

class WebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path != "/":
            return

        day = self.headers.get("day")
        month = self.headers.get("month")
        year = self.headers.get("year")
        time = datetime.datetime(year, month, day)

        density = {}
        for hour in range(24):
            density[str(hour)] = get_density(time.hour, time.weekday(), time.isocalendar()[1])

        json_text = json.dump(density)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json_text, "utf-8"))
        self.send_response(200)

def get_density(hour, weekday, week_number):
    return 5

try:
    webserver = HTTPServer(("localhost", 8080), WebServer)
    webserver.serve_forever()
except KeyboardInterrupt:
    print("KeyboardInterrupt.")
