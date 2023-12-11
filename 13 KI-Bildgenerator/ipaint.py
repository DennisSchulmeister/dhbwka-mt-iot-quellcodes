#! /usr/bin/env python3
"""
Startskript des Programms.
"""

from ipaint.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass