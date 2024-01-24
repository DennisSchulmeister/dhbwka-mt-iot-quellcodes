# Allgemeine Helfer
import dotenv, os, time, logging

# Hardwarezugriffe
import board
import adafruit_bmp280
import digitalio

# Kommunikation mit ThingsBoard
from tb_device_mqtt import TBDeviceMqttClient

enabled = True
alarm   = False

def receive_shared_attributes(attributes, *args):
    """
    Geteilte Attribute vom Server empfangen.
    """
    shared_attributes = attributes["shared"] if "shared" in attributes else attributes

    if "enabled" in shared_attributes:
        global enabled
        enabled = shared_attributes["enabled"]
    
    if "alarm" in shared_attributes:
        global alarm
        alarm = shared_attributes["alarm"]

def main():
    """
    Hauptfunktion
    """
    # Logging einrichten
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

    # Verbindung mit ThingsBoard herstellen
    dotenv.load_dotenv()
    
    logging.info(f"Stelle Verbindung zum Backend her: mqtt://{os.environ['TB_HOST']}:{os.environ['TB_PORT']}")

    tb_client = TBDeviceMqttClient(
        host     = os.environ["TB_HOST"],
        port     = int(os.environ["TB_PORT"]),
        username = os.environ["TB_TOKEN"],
    )

    tb_client.connect()

    tb_client.request_attributes(shared_keys=["enabled", "alarm"], callback=receive_shared_attributes)
    tb_client.subscribe_to_attribute("enabled", callback=receive_shared_attributes)
    tb_client.subscribe_to_attribute("alarm", callback=receive_shared_attributes)

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