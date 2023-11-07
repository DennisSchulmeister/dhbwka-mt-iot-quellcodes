Selbsfahrendes Fahrzeug
=======================

Dieses Beispiel zeigt, wie ein autonomer Roboter bzw. ein selbstfahrendes
Fahrzeug in Python realisiert werden kann. Der Roboter führt hierfür mehrere,
nebenläufige Prozesse aus, um mit den ihm zur Verfügung stehenden Sensoren
seine Umwelt warzunehmen und dieses Eingaben in Aktionen umzusetzen.

Es gibt zwei Varianten des Beispiels hier:

 1. Ordner `Device`: Reale Hardware-Implementierung auf Basis des
    [OSOYOO Robot Car V2 for Raspberry Pi](https://osoyoo.com/category/osoyoo-raspi-kit/osoyoo-car-v2-pi/)
    Bausatzes.

 2. Ordner `Simulation`: Abgespeckte Variante, in welcher die Hardwarebausteine
    mit [tkgpio](https://github.com/wallysalami/tkgpio) simuliert werden.
    Dieses Beispiel kann auf dem eigenen Laptop ohne Raspberry Pi ausgeführt werden.

Die erste Variante ist vollständig implementiert, inklusive mehreren Strategien
für das autoname Fahren sowie einer Möglichkeit, den Roboter via UDP aus der
Ferne zu steuern. Die zweite Variante besitzt eine ähnliche Struktur, wurde aber
an vielen Stellen vereinfacht, um innerhalb der Vorlesungszeit erarbeitet werden
zu können. Sie beruht zusätzlich auf Coroutinen und dem asyncio-Framework, während
die erste Variante ein eigenes, simples Task Scheduling implementiert.

![Foto](Device/foto.jpg)
![Screenshot](Simulation/screenshot.png)