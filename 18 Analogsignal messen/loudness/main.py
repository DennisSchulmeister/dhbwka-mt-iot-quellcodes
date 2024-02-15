"""
Beispiel zur Messung der Umgebungslautstärke mit dem KY-037 Mikrofon über den
KY-053 A/D-Konverter.
"""

import curses
import time
import busio
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn

ADC_CLOCK = 3
ADC_SDATA = 2

def main():
    try:
        # Terminal initialisieren
        screen = curses.initscr()

        # A/D-Konverter initialisieren
        i2c_bus = busio.I2C(ADC_CLOCK, ADC_SDATA)
        ad_converter = ADC.ADS1115(i2c_bus)
        adc_channel0 = AnalogIn(ad_converter, ADC.P0)

        # Endlosschleife, damit das Programm weiterläuft
        while True:
            # Lautstärke messen
            voltage = adc_channel0.voltage
            value = adc_channel0.value
            bar_len = int((value - 590) / 5.0)

            # Ergebnis anzeigen
            screen.clear()
            screen.addstr(0, 0, "Spannung: %s V" % voltage)
            screen.addstr(0, 40, "Messwert: %s" % value)
            screen.addstr(1, 0, "#" * bar_len)
            screen.refresh()

            # Kurz warten
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    curses.endwin()
    i2c_bus.deinit()
