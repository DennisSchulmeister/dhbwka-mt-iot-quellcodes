from carbot_rc.gui import MainWindow
from carbot_rc.remote import RemoteConnection

def main():
    """
    Vom Startskript aufgerufene Hauptfunktion des Programms. Hier wird das
    User Interface initialisiert und gestartet.
    """
    print("carbot_rc sagt Hallo!")

    connection = RemoteConnection(host="", port=6789, remote_port=9876, update_frequency=10)
    window = MainWindow(connection)
    window.mainloop()