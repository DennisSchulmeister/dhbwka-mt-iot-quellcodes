"""
Geklautes Beispiel von pycamera2: Auf dem Port 8000 kann im Browser
ein Livestream von der Fahrzeugkamera betrachtet werden.
"""

import io
import logging
import socketserver
from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

from libcamera import Transform

PAGE = """\
<html>
    <head>
        <title>Fahrzeug-Kamera</title>
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100vh;
            }

            body {
                display: flex;
                justify-content: center;
                align-content: stretch;
                align-items: stretch;
            }
        </style>
    </head>
    <body>
        <img src="stream.mjpg" />
    </body>
</html>
"""

output = None

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        global output

        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()

            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame

                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def main():
    """
    Hauptfunktion zum Starten des Servers.
    """
    global output
    
    picam2 = Picamera2()

    picam2_config = {
        "size": (640, 480),
    }

    # FIXME: Kamerabild ist spiegelverkehrt (links/rechts vertauscht)
    picam2.configure(picam2.create_video_configuration(picam2_config, transform = Transform(vflip=True)))
    output = StreamingOutput()
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    print("Starte Webserver auf Port 8000")

    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        picam2.stop_recording()