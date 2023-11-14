#!/usr/bin/env python

def main():
    name = ""

    print("\033c", end='')

    while not name:
        name = input("Wie heißt du? ")

    print(f"Hallo {name}!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
