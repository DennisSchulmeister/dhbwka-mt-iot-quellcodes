# https://docs.circuitpython.org/en/latest/shared-bindings/board/index.html
# https://docs.circuitpython.org/en/latest/shared-bindings/busio/index.html
# https://docs.circuitpython.org/projects/pca9685/en/latest/index.html
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

from carbot.motor import PCA9685Motor
from carbot.vehicle import Vehicle
from carbot.sensors.obstacle import ObstacleSensor
from carbot.sensors.direction import DirectionServo
from carbot.sensors.line import LineSensor
from carbot.drive.direction_change import any, limit, random_interval, on_obstacle, print_change
from carbot.drive.strategy import BackAndForthDrive, RandomDrive, FollowLineDrive
from carbot.remote.udp import UDPRemoteControl
from carbot.sound.player import SoundPlayer

def main():
    """
    Vom Startskript aufgerufene Hauptfunktion des Programms. Hier werden die
    Objekte zur Steuerung des Fahrzeug konfiguriert und miteinander verknüpft.
    Anschließend wird die in der Klasse `Vehicle` implementierte Hauptschleife
    gestartet.
    """
    print("carbot sagt Hallo!")

    # pigpio-Bibliothek für höhere Genauigkeit verwenden, falls installiert
    try:
        from gpiozero.pins.pigpio import PiGPIOFactory
        from gpiozero import Device
        Device.pin_factory = PiGPIOFactory()
        print("Benutze pigpio für höhere Genauigkeit")
    except:
        pass

    # PCA9685-Baustein für die PWM-Steuerung der Motoren
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 60

    # Fahrzeug starten
    motor_left  = PCA9685Motor(pca, forward=24, backward=23, pwmChannel=0)
    motor_right = PCA9685Motor(pca, forward=22, backward=27, pwmChannel=1)

    vehicle = Vehicle(motor_left, motor_right)

    vehicle.add_sensor("sensor:line", LineSensor([5, 6, 13, 19, 26], line_color=LineSensor.BLACK))
    vehicle.add_sensor("sensor:obstacle", ObstacleSensor(trigger=20, echo=21, min_cm=10, max_cm=100))
    vehicle.add_sensor("sensor:direction", DirectionServo(pca, pwmChannel=15))
    vehicle.add_sensor("drive:random", RandomDrive(print_change(limit(any(on_obstacle(vehicle, 0.75), random_interval(10, 30))))))
    vehicle.add_sensor("drive:backforth", BackAndForthDrive(print_change(limit(any(on_obstacle(vehicle, 0.9), random_interval(10, 30))))))
    vehicle.add_sensor("drive:line", FollowLineDrive())
    vehicle.add_sensor("sound:player", SoundPlayer())
    vehicle.add_sensor("remote:udp", UDPRemoteControl("", 9876))

    vehicle.get_sensor("drive:random").disable()
    vehicle.get_sensor("drive:backforth").disable()
    vehicle.get_sensor("drive:line").disable()

    try:
        vehicle.loop_forever()
    except:
        vehicle.stop()
