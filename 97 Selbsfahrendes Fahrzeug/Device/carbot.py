#! /usr/bin/env python3
"""
Startskript für das carbot-Program
"""

from carbot.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass