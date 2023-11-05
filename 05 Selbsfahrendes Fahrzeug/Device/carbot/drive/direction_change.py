import random, time

def print_change(strategy):
    """
    Protokollzeile auf der Konsole, wenn die Strategie einen
    Richtungswechsel auslöst.
    """
    while True:
        try:
            change = strategy.__next__()
        except:
            pass

        if change:
            print("Änderung der Fahrtrichtung")

        yield change

def limit(strategy, not_before_s=1):
    """
    Sicherstellen, dass nicht öfters als einmal alle N Sekunden
    ein Richtungswechsel erfolgt.
    """
    prev_change_time = 0

    while True:
        curr_time = time.monotonic()
        
        try:
            change = strategy.__next__()
        except:
            pass

        if change:
            if curr_time - prev_change_time < not_before_s:
                yield False
            else:
                prev_change_time = curr_time
                yield True
        else:
            yield False

def any(*strategies):
    """
    Kombination aus mehreren Strategien, zum Beispiel:
    
        any(fixedInterval(5), onObstacle(vehicle, 0.8))
    
    Ein Richtungswechsel findet immer statt, wenn einer der übergebenen
    Strategien ihn auslöst.
    """
    while True:
        for strategy in strategies:
            try:
                change = strategy.__next__()
            except:
                pass

            if change:
                break
        
        yield change

def fixed_interval(seconds):
    """
    Richtungswechsel nach festem Zeitintervall.
    """
    prev_time = 0

    while True:
        curr_time = time.monotonic()

        if (curr_time - prev_time) >= seconds:
            yield True
        else:
            yield False

def random_interval(min_seconds, max_seconds):
    """
    Richtungswechsel nach zufälligem Zeitintervall.
    """
    prev_time = 0
    seconds = random.randint(min_seconds, max_seconds)

    while True:
        curr_time = time.monotonic()

        if (curr_time - prev_time) >= seconds:
            seconds = random.randrange(min_seconds, max_seconds)
            prev_time = curr_time
            print(f"Nächster Richtungswechsel spätestens in {seconds} Sekunden")
            yield True
        else:
            yield False

def on_obstacle(vehicle, max_pushback):
    """
    Richtungswechsel bei Hinderniss.
    """
    yield True

    while True:
        if vehicle.speed_total >= 0 and vehicle.obstacle_pushback >= max_pushback:
            yield True
        if vehicle.speed_total < 0 and vehicle.obstacle_pushback <= max_pushback * -1:
            yield True
        else:
            yield False
