import logging
import random
from datetime import datetime

from src.Json import JsonManager
from Xml import XmlManager, XmlExtract
from src.AppleScript import AppleScripts


class PlaylisterManager:
    """ Manages the creation of playlists """

    def __init__(self, playlister_name: str):
        self.playlister_name: str = playlister_name.lower()
        self.structure: dict = {
            'daily album': self.daily_album
        }

    def create(self) -> None:
        structure: classmethod = self.structure.get(self.playlister_name)
        if structure:
            structure()
        else:
            logging.error(f"New file needs to be made with {self.playlister_name}")

    def daily_album(self) -> None:
        playlister = PlaylisterCreation(self.playlister_name)
        playlister.create_playlist(
            step1=playlister.filter_albums,
            step2=playlister.select_random_album,
            step3=playlister.update_json
        )


class PlaylisterCreation:
    """ Generates a new playlist based on user selection"""
    def __init__(self, playlister_name: str):
        self.playlister_name: str = playlister_name.title()
        self.current_date: str = datetime.now().strftime('%d-%m-%Y')
        self.json_manager = JsonManager(playlister_name)
        self.json_load: dict = self.json_manager.load()
        xml_manager = XmlManager()
        self.xml_grab = XmlExtract(xml_manager)
        self.album_tracks: dict = self.xml_grab.album_tracks_with_artists()

    def create_playlist(self, step1, step2, step3) -> None:
        if self.limit_daily():
            return

        filtered_albums = step1()
        self.reset_album_list(filtered_albums)
        self.log_filtered_albums(filtered_albums)

        if filtered_albums:
            selected_album = step2(filtered_albums)
            new_playlist_name = self.name_playlist(selected_album)
            self.applescript(new_playlist_name, *selected_album)
            step3(new_playlist_name, *selected_album)

    def limit_daily(self):
        json_date: str = self.json_load["Album of the Day JSON file"].get("Last updated")
        limit: bool = self.json_load["Config"].get("Limit one album per day")

        if limit and self.current_date == json_date:
            logging.info(f"{self.playlister_name} already created today")
            return True
        return False

    def filter_albums(self) -> list[tuple[str, str]]:
        """ Filters the albums to meet minimum track count """
        used_albums: dict = self.json_load["Albums used"]
        min_album_tracks: int = self.json_load["Config"].get("Minimum album tracks")
        cycle_albums: bool = self.json_load["Config"].get("Cycle albums")

        eligible_albums: list = [album_artist for album_artist, count in self.album_tracks.items()
                                 if count >= min_album_tracks]

        if cycle_albums:
            eligible_albums: list = [
                album_artist for album_artist in eligible_albums
                if (f"{album_artist[0]} - {album_artist[1]}" not in used_albums)
            ]

        return eligible_albums

    def reset_album_list(self, filtered_albums: list):
        """ Clear JSON list if all albums used """
        if len(filtered_albums) == 1:
            self.json_load["Albums used"] = []
            logging.info("Cycled all albums.... Resetting ⏮️")

    @staticmethod
    def log_filtered_albums(filtered_albums):
        """ Log filtered albums in a list """
        list_filtered_albums = "\n      ".join(f"{album}" for album, artist in sorted(filtered_albums))
        logging.info("(%s) ALBUMS AVAILABLE: \n      %s", len(filtered_albums), list_filtered_albums)

    def name_playlist(self, selected_album):
        album_for_playlist_name: bool = self.json_load["Config"].get("Use album for playlist name")
        new_playlist_name: str = self.json_load["Config"].get("Playlist name")

        if album_for_playlist_name:
            new_playlist_name = selected_album[0]

        return new_playlist_name

    @staticmethod
    def select_random_album(filtered_albums):
        """ Picks a random album from the filtered list"""
        album_picked, artist_picked = random.choice(filtered_albums)

        log_album_picked = f"{album_picked} - {artist_picked}"
        logging.info("ALBUM RANDOMLY PICKED:\n      💿 '%s'", log_album_picked)

        return album_picked, artist_picked

    def applescript(self, new_playlist_name, album_picked, artist_picked):
        """ Run applescripts to interact with Music app """
        json_playlist_name: str = self.json_load["Config"].get("Playlist name")
        apple = AppleScripts(new_playlist_name, json_playlist_name, album_picked, artist_picked)

        # Delete old playlist
        if json_playlist_name != new_playlist_name:
            apple.delete_old_playlist()

        # Create and add album to playlist
        apple.create_or_clear_playlist()
        apple.add_album_to_playlist()

    def update_json(self, new_playlist_name, album_picked, artist_picked):
        """ Update the JSON file """
        self.json_load["Album of the Day JSON file"]["Last updated"] = self.current_date
        self.json_load["Album of the Day JSON file"]["Current album"] = f"{album_picked} - {artist_picked}"
        self.json_load["Albums used"].append(f"{album_picked} - {artist_picked}")
        self.json_load["Config"]["Playlist name"] = new_playlist_name

        self.json_manager.save(self.json_load)
