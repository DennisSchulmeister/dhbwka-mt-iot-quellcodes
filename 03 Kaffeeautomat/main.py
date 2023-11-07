import time

def clear_screen():
    """
    Konsolenausgaben löschen
    """
    print("\033c", end="", flush=True)

def make_drink(drink: str):
    """
    Zubereitung und Ausgabe eines Getränks. Bekommt den Namen des Getränks als String übergeben.
    """
    print()
    print("Zubereitung läuft", end="", flush=True)

    for i in range(15):
        time.sleep(0.5)
        print(".", end="", flush=True)

    print()
    print(f"{drink} – Bitte schön!")
    time.sleep(4)

def main():
    """
    Hauptprogramm
    """
    while True:
        clear_screen()

        print("====================================================================")
        print("= Der Python Kaffeeautomat – besser als das Ding im Casino allemal =")
        print("====================================================================")
        print()
        print("Heute im Angebot:")
        print()
        print(" [1] Kaffee schwarz")
        print(" [2] Cappuccino")
        print(" [3] Latte Macchiato")
        print(" [4] Espresso")
        print(" [5] Schokoccino")
        print(" [6] Kaba")
        print(" [7] Tee")
        print(" [E] ENDE")
        print()

        chosen_drink = input("Auswahl: ")

        match chosen_drink:
            case "1":
                make_drink("Kaffee")
            case "2":
                make_drink("Cappuccino")
            case "3":
                make_drink("Latte Macchiato")
            case "4":
                make_drink("Espresso")
            case "5":
                make_drink("Schokoccino")
            case "6":
                make_drink("Kaba")
            case "7":
                make_drink("Tee")
            case "E" | "e":
                break
            case _:
                print("Falsche Eingabe")
                time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
