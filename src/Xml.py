import subprocess
import plistlib  # Parse apple typed XML files
import logging
import os


class XmlManager:
    def __init__(self):
        self.home_dir: str = os.path.expanduser('~')
        self.music_dir: str = os.path.join(self.home_dir, 'Music/Music')
        self.xml_file: str = os.path.join(self.home_dir, 'Music/Music/Playlister.xml')
        self.music_xml_exporter: str = (
            f'music-library-exporter export --music_media_dir "{self.music_dir}"'
            f' --output_path "{self.music_dir}"/Playlister.xml'
        )

    def refresh_file(self) -> None:
        """Delete XML file"""
        if os.path.exists(self.xml_file):
            os.remove(self.xml_file)
        else:
            logging.info('Creating brand new XML file... 📄')

        self.create_file()

    def create_file(self) -> None:
        """Create new XML file"""
        try:
            subprocess.run(
                self.music_xml_exporter,
                shell=True,  # Run command in shell (Higher permissions)
                check=True,  # Raise exception if error
                stdout=subprocess.DEVNULL,  # Hide output
                stderr=subprocess.PIPE  # Capture errors
            )
            logging.info('Refreshed XML file 🔄')
        except subprocess.CalledProcessError as error:
            logging.error(f'Issue running music-library-exporter: {error.stderr.decode()}')
            raise

    def load(self) -> dict:
        """Load XMl file for parsing data with plistlib (Apple XML format)"""
        try:
            with open(self.xml_file, 'rb') as xml_file:
                return plistlib.load(xml_file)
        except plistlib.InvalidFileException as error:
            logging.error(f"Error loading XML file: {error}")
            raise


class XmlExtract:
    def __init__(self, xml_manager: XmlManager):
        self.xml_load: dict = xml_manager.load()

    def album_tracks_with_artists(self) -> dict:
        """Extract album tracks with artists from XML file"""
        album_tracks: dict = {}

        for track_id, track in self.xml_load['Tracks'].items():
            album: str = track.get('Album')
            artist: str = track.get('Artist')

            # Ensure the track has both an album and an artist
            if album and artist:
                album_and_artist: tuple = (album, artist)

                # Count the number of tracks for each album
                if album_and_artist not in album_tracks:
                    album_tracks[album_and_artist] = 0
                album_tracks[album_and_artist] += 1

        return album_tracks
