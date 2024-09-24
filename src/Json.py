import os
import json
import logging
from datetime import datetime


class JsonManager:
    def __init__(self, playlister_name: str):
        self.playlister_library = '../data/Playlist\'er library'
        self.playlister_name: str = playlister_name.lower()
        self.playlister_file: str = os.path.join(self.playlister_library + '/' + playlister_name + ".json")
        self.structure: dict = {
            'daily album': JsonDefaults.daily_album
        }

    def load(self) -> dict:
        """Load JSON file if exists"""
        JsonManager.check_folder(self)

        if os.path.exists(self.playlister_file):
            with open(self.playlister_file, "r") as file:
                return json.load(file)
        else:
            self.create_new_file()

    def check_folder(self) -> None:
        folder_exists = os.path.exists(self.playlister_library)

        if not folder_exists:
            os.makedirs(self.playlister_library)
            logging.info('No Playlist folder found! \n'
                         'Creating new folder.')

    def create_new_file(self) -> None:
        """Create new JSON based on a structure"""
        structure = self.structure.get(self.playlister_name)

        if structure:
            playlist_structure = structure()
            self.save(playlist_structure)
        else:
            logging.info(f"{self.playlister_name} "
                         f"does not have a related structure, need generate new structures for this")

    def save(self, data) -> None:
        """Save JSON file with updated data"""
        with open(self.playlister_file, "w") as JS_file:
            json.dump(data, JS_file, indent=4)
            logging.info("JSON FILE UPDATED 📄")


class JsonDefaults:

    @staticmethod
    def daily_album():
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
