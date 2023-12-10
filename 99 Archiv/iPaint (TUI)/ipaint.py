#! /usr/bin/env python3
"""
Startskript des Programms.
"""

from ipaint.main import IPaintApp

if __name__ == "__main__":
    #import pudb; pu.db
    app = IPaintApp()
    app.run()
