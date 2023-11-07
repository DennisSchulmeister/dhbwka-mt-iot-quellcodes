#! /usr/bin/env python3
"""
Startskript für den camera-Server.
"""

from camera.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass