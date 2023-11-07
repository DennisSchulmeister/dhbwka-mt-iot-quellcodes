import asyncio

from gpiozero import Motor
from carbot_sim.vehicle import Vehicle
from carbot_sim.utils import UpdateFrequency
from carbot_sim.sensors.direction import DirectionServo
from carbot_sim.sensors.obstacle import ObstacleSensor
from carbot_sim.sensors.line import LineSensor
from carbot_sim.drive.random import RandomDrive
from carbot_sim.drive.manual import ManualDrive
    
async def main():
    """
    Vom Startskript aufgerufene Hauptfunktion des Programms. Hier werden die Objekte zur Ansteuerung
    der Hardwarebausteine erzeugt und die nebenläufigen Tasks mit den Fahrzeugfunktionen gestartet.
    """
    print("carbot_sim sagt Hallo!")

    motor_left = Motor(forward=24, backward=23, pwm=True)
    motor_right = Motor(forward=22, backward=27, pwm=True)

    vehicle = Vehicle(motor_left, motor_right)
    asyncio.create_task(vehicle.drive(UpdateFrequency(2)))

    vehicle.add_task("DirectionServo", DirectionServo(15, UpdateFrequency(2), vehicle))
    vehicle.add_task("ObstacleSensor", ObstacleSensor(UpdateFrequency(2), vehicle, trigger=20, echo=21, min_cm=10, max_cm=80))
    vehicle.add_task("LineSensor", LineSensor(UpdateFrequency(2), vehicle))     # AUFGABE: LineSensor implementieren und hier den Aufruf anpassen
    vehicle.add_task("RandomDrive", RandomDrive(UpdateFrequency(2), vehicle, min_count=8, max_count=60))
    vehicle.add_task("ManualDrive", ManualDrive(UpdateFrequency(2), vehicle))   # AUFGABE: ManualDrive implementieren und hier den Aufruf anpassen

    # Workaround, damit die asyncio Event Loop tatsächlich laufen kann
    while True:
        await asyncio.sleep(0)