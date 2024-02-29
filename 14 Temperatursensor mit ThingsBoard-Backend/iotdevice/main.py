# Allgemeine Helfer
import dotenv, os, time, logging

# Hardwarezugriffe
import board
import adafruit_bmp280
import digitalio

# Kommunikation mit ThingsBoard
from tb_device_mqtt import TBDeviceMqttClient

enabled   = True
alarm     = False
tb_client = None

def receive_shared_attributes(attributes, *args):
    """
    Geteilte Attribute vom Server empfangen.
    """
    shared_attributes = attributes["shared"] if "shared" in attributes else attributes
    logging.info(f"Empfange geteilte Attribute: {shared_attributes}")

    if "enabled" in shared_attributes:
        global enabled
        enabled = shared_attributes["enabled"]
    
    if "alarm" in shared_attributes:
        global alarm
        alarm = shared_attributes["alarm"]

def handle_rpc_request(client, request_body):
    """
    RPC (Remote Procedure Call) Anfrage, bei welcher der Server den Raspi auffordert,
    eine bestimmte Aktion auszuführen, bearbeiten.
    """
    logging.info(f"RPC-Anfrage vom Server empfangen: {request_body}")

    # Workaround für fehlende Funktion im Thingsboard-Dashboard. Dort können Control Widgets
    # wie ein An/Aus-Schalter zwar den Wert eines Shared Attributes anzeigen aber nicht ändern.
    # Sie können nur einen RPC-Request an das Device schicken. Wir ändern den Wert daher hier
    # auf dem Device durch einen entsprechende Anfrage an den Server.
    #
    # ACHTUNG: Damit das funktioniert, muss die Root Rule Chain in ThingsBoard angepasst werden.
    # Die hier gesendeten Attribute werden standardmäßig nämlich als "Device Attributes" gespeichert.
    # Wir müssen sie aber als "Shared Attributes" speichern!
    if request_body["method"] == "setValue":
        attribute = request_body["params"]["attribute"]
        value     = request_body["params"]["value"]

        if attribute:
            logging.info(f"Setze Attribut {attribute} auf {value}")
            tb_client.send_attributes({attribute: value})

def main():
    """
    Hauptfunktion
    """
    # Logging einrichten
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

    # Verbindung mit ThingsBoard herstellen
    dotenv.load_dotenv()
    
    logging.info(f"Stelle Verbindung zum Backend her: mqtt://{os.environ['TB_HOST']}:{os.environ['TB_PORT']}")

    global tb_client

    tb_client = TBDeviceMqttClient(
        host     = os.environ["TB_HOST"],
        port     = int(os.environ["TB_PORT"]),
        username = os.environ["TB_TOKEN"],
    )

    tb_client.connect()

    tb_client.request_attributes(shared_keys=["enabled", "alarm"], callback=receive_shared_attributes)
    tb_client.subscribe_to_all_attributes(receive_shared_attributes)
    tb_client.set_server_side_rpc_request_handler(handle_rpc_request)

    # Objekte für die Hardwarezugriffe erzeugen
    logging.info("Initialisiere Hardwarebausteine")

    i2c = board.I2C()
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    bmp280.sea_level_pressure = 1013.25

    buzzer = digitalio.DigitalInOut(board.D18)
    buzzer.direction = digitalio.Direction.OUTPUT

    # Sensordaten periodische auslesen und an das Backend senden
    global enabled, alarm

    while True:
        if enabled:
            telemetry = {
                "temperature": bmp280.temperature,
                "pressure":    bmp280.pressure,
                "altitude":    bmp280.altitude,
            }

            logging.info(f"Sende Telemetriedaten: {telemetry}")
            tb_client.send_telemetry(telemetry)
        
        if alarm:
            logging.warning("Alarm aktiv!")
        
        buzzer.value = alarm

        time.sleep(2)