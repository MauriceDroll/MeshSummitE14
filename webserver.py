# Imports
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

from data import *
from startpilot import *

# Webserver to handle traffic prediction request
class WebServer(BaseHTTPRequestHandler):
    # Handles GET requests on path "/"
    def do_GET(self):
        if self.path != "/":
            return

        # Get the date the of request
        day = self.headers.get("day")
        month = self.headers.get("month")
        year = self.headers.get("year")
        time = datetime.datetime(year, month, day)

        # Get traffic predicions for all 24 hours
        density = {}
        for hour in range(24):
            density[str(hour)] = get_density(hour, time.weekday(), time.isocalendar()[1])

        # Send json response data
        json_text = json.dump(density)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json_text, "utf-8"))
        self.send_response(200)

# Gets the traffic density prediction for a timestamp
def get_density(hour, weekday, week_number):
    weather_data = WeatherData()
    tensor, time = weather_to_tensor(weather_data)
    return predivtive_traffic(tensor)

# Start webserver on http://localhost:8080
try:
    webserver = HTTPServer(("localhost", 8080), WebServer)
    webserver.serve_forever()
except KeyboardInterrupt:
    print("KeyboardInterrupt.")
