def input_nr(prompt):
    """
    Benutzer auffordern, eine Zahl einzugeben. Wiederholt die Aufforderung, bis eine
    gültige Zahl eingegeben wurde und liefert diese dann als Ergebnis zurück.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            pass
    

def input_op(prompt):
    """
    Benutzer auffordern, einen Rechenoperator einzugeben. Erlaubt sind +, -, *, / und \.
    Wiederholt die Aufforderung, bis ein gültiges Zeichen eingegeben wurde und gibt dieses
    dann zurück.
    """
    allowed = "+-*/\\"

    while True:
        operator = input(prompt).strip()

        if operator in allowed:
            break
    
    return operator

def main():
    """
    Hauptprogramm
    """
    print("\033c", end="", flush=True)

    print("=============================")
    print("= Der Python Taschenrechner =")
    print("=============================")
    print()
    print("Zum Beenden bitte Strg+C drücken.")
    print()

    while True:        
        number1  = input_nr("Zahl 1: ")
        operator = input_op("Operator: ")
        number2  = input_nr("Zahl 2: ")

        match operator:
            case "+":
                result = number1 + number2
            case "-":
                result = number1 - number2
            case "*":
                result = number1 * number2
            case "/" | "\\":
                result = number2 / number2
            case _:
                continue
        
        print(f"Ergebnis: {result}")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
