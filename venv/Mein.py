import random
import logging
from datetime import datetime
from Xml import Manager, Extract
from Json import jsonfunctions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s >\n %(message)s\n', datefmt='%H:%M:%S')

# Load your iTunes XML file
xml_file = load_xml()

# Create a dictionary to count tracks for each album
album_tracks = {}
min_tracks = 5
playlist_name = ""

js_file = jsonfunctions({})
JSON = js_file.load_json()
Albums_used = JSON["Albums used"]
JSON_playlist_name = JSON["Album of the Day JSON file"].get("Playlist name", "")

# Filter albums to meet the minimum track count
filtered_albums = [
    album_and_artist for album_and_artist, count in album_tracks.items()
    if count >= min_tracks and f"{album_and_artist[0]} - {album_and_artist[1]}" not in Albums_used
]

if len(filtered_albums) == 1:
    JSON["Albums used"] = []
    logging.info("Cycled all albums.... Resetting 🔄")

list_filtered_albums = "\n      ".join(f"{album}" for album, artist in sorted(filtered_albums))
logging.info("(%s) ALBUMS AVAILABLE: \n      %s", len(filtered_albums), list_filtered_albums)

# Select a random album from the filtered list
if filtered_albums:
    album_picked, artist_picked = random.choice(filtered_albums)
    playlist_name = album_picked
    log_album_picked = f"{album_picked} - {artist_picked}"
    logging.info("ALBUM RANDOMLY PICKED:\n      💿 '%s'", log_album_picked)

apple = applescripts(playlist_name, JSON_playlist_name, album_picked, artist_picked)

if JSON_playlist_name != playlist_name:
    apple.delete_old_playlist()

apple.create_or_clear_playlist()
apple.add_album_to_playlist()

# Update the JSON
JSON["Album of the Day JSON file"]["Last updated"] = datetime.now().strftime('%d-%m-%Y')
JSON["Album of the Day JSON file"]["Playlist name"] = playlist_name
JSON["Album of the Day JSON file"]["Current album"] = f"{album_picked} - {artist_picked}"
JSON["Albums used"].append(f"{album_picked} - {artist_picked}")

js_file.JSON = JSON
js_file.update_json()