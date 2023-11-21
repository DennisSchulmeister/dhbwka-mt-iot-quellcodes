#!/usr/bin/env python

def main():
    """Hauptfunktion"""
    # Angaben zu Hösrspielfiguren: Name, Beschreibung, Anzahl bisheriger Sprecher (November 2023)
    benjamin = ("Benjamin Blümchen", "Sprechender Elefant", 2)
    otto = ("Otto", "Benjamins bester Freund", 3)

    person_list = [benjamin, otto, ("Theodor Tierlieb", "Zoobesitzer", 4)]
    person_list.append(("Karla Kolumna", "Rasende Reporterin", 2))

    karl = {
        "name": "Karl",
        "role": "Zoowärter",
        "n_voice_actors": 3,
    }

    buergermeister = dict(name="Bürgermeister", rolle="Gegenspieler unserer Freunde", n_voice_actors=4)

    # Anzeige der Listen und Tupel
    print("\033c", end="", flush=True)
    print("-----------------------------------")
    print("Schleifen über die Listen und Tupel")
    print("-----------------------------------")
    print()

    for person in person_list:
        for value in person:
            print(value)

        print(", ".join([str(x) for x in person]))
        print()
    
    # Anzeige mit Entpacken der Tupel
    print("---------------------------------")
    print("Direktes Entpacken der Tupelwerte")
    print("---------------------------------")
    print()

    for person in person_list:
        name, role, n_voice_actors = person
        print(f"{name}: {role}, {n_voice_actors} Sprecher")

    print()
    print("-------------------------------")
    print("Zugriff auf Dictionary-Einträge")
    print("-------------------------------")
    print()

    print(f"{karl['name']}: {karl['role']}, {karl['n_voice_actors']} Sprecher")
    print(f"{buergermeister['name']}: {buergermeister['rolle']}, {buergermeister['n_voice_actors']} Sprecher")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass