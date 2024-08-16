import os
import json
import logging
from datetime import datetime

file_path = "Daily Album.json"

class jsonfunctions:
    def __init__(self, JSON):
        self.JSON = JSON

    def load_json(self):
        if os.path.exists(file_path):
            with open(file_path, "r") as JS_file:
                return json.load(JS_file)
        else:
            return {
                "Album of the Day JSON file": {
                    "Last updated": datetime.now().strftime('%d-%m-%Y'),
                    "Current album": ""
                },
                "Albums used": [],
                "Config": {
                    "Playlist name": "Daily Album",
                    "Use album for playlist name": True,
                    "Minimum album tracks": 5,
                    "Cycle albums": True,
                    "Limit one album per day": False
                }
            }

    def update_json(self):
        with open(file_path, "w") as JS_file:
            json.dump(self.JSON, JS_file, indent=4)
            logging.info("JSON FILE UPDATED 📄")