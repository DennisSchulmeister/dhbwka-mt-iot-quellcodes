#!/usr/bin/env python

import logging, random, time

def main():
    """Hauptfunktion"""
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
    logging.info("Das Programm startet, zum Beenden Strg+C drücken!")

    while True:
        wait_time_s = random.randint(1, 5)
        time.sleep(wait_time_s)

        logging.info(f"Es sind jetzt {wait_time_s} Sekunden vergangen.")
        logging.info("Zeit für eine weitere Meldung im Protokoll.")
        logging.info("")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass