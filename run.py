#!/usr/bin/env python3

"""
Exports an instance of the Dawdle app. If run with the main function,
the Flask development server will start running the app on
'localhost:5000'.
"""

from dawdle import create_app

APP = create_app()

if __name__ == "__main__":
    APP.run()
