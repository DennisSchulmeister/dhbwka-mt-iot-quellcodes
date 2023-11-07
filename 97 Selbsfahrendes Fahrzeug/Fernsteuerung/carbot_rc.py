#! /usr/bin/env python3
"""
Startskript für das carbot_rc-Program
"""

from carbot_rc.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass