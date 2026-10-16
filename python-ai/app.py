
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_KEY = os.environ.get("GEMINI_API_KEY")

FALLBACK_CHANT = (
    "Keep your goals shining bright,\n"
    "Learn and grow with all your might!\n"
    "Step by step, you'll reach the top,\n"
    "Believe in you and never stop!"
)


class ChantHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        topic = query.get("topic", ["study"])[0].strip()

        if urlparse(self.path).path == "/favicon.ico":
            self.send_text(204, "")
            return

        if not topic or len(topic) > 100:
            self.send_text(
                400,
                "Please enter a topic of up to 100 characters."
            )
            return

        if not API_KEY:
            self.send_text(200, FALLBACK_CHANT)
            return

        prompt = (
            f"Create an original, uplifting chant about {topic}. "
            "Keep it to 4 short lines, easy to remember, positive, "
            "and suitable for students. Return only the chant."
        )

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        request = Request(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": API_KEY
            },
            method="POST"
        )

        try:
            with urlopen(request, timeout=60) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            chant = data["candidates"][0]["content"]["parts"][0]["text"]
            self.send_text(200, chant.strip())

        except HTTPError as error:
            print("Gemini API HTTP error:", error.code)
            print(error.read().decode("utf-8"))
            self.send_text(200, FALLBACK_CHANT)

        except (
            URLError,
            TimeoutError,
            KeyError,
            IndexError,
            ValueError
        ) as error:
            print("AI request failed:", type(error).__name__)
            self.send_text(200, FALLBACK_CHANT)

    def send_text(self, status, message):
        body = message.encode("utf-8")
        self.send_response(status)
        self.send_header(
            "Content-Type",
            "text/plain; charset=utf-8"
        )
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        if body:
            self.wfile.write(body)


server = HTTPServer(("localhost", 5000), ChantHandler)
print("AI Chant Generator Python server running at http://localhost:5000")
server.serve_forever()
