#! /usr/bin/env python

from myapp.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass