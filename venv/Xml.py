import subprocess
import plistlib
import logging
import os

# music-library-exporter export --music_media_dir "/Users/aidanosullivan/Music/Music/Media" --output_path "/Users/aidanosullivan/Music/Music/GeneratedLibrary.xml"
#media_dir = os.path.join(home_dir, 'Music/Music/Media.localised/Music')

class Manager:
    def __init__(self):
        self.home_dir = os.path.expanduser('~')
        self.music_dir = os.path.join(self.home_dir, 'Music/Music')
        self.xml_file = os.path.join(self.home_dir, 'Music/Music/Playlister.xml')
        self.music_xml_exporter = (
            f'music-library-exporter export --music_media_dir "{self.music_dir}"'
            f' --output_path "{self.music_dir}"/Playlister.xml'
        )

    def update_xml_file(self):
        # Remove old XML file
        if os.path.exists(self.xml_file):
            os.remove(self.xml_file)
        else:
            logging.info('Creating new XML file... 📄')

        # Generate new XML file
        try:
            subprocess.run(
                self.music_xml_exporter,
                shell=True,
                stdout=subprocess.DEVNULL # Hide output
            )
        except Exception as e:
            logging.error(f'Issue running music-library-exporter: {e}')

    def load_xml(self):
        #replace_xml()
        try:
            with open(self.xml_file, 'rb') as f:
                return plistlib.load(f)
        except FileNotFoundError:
            logging.error("No '.xml' file found ❌")
            exit()


class Extract:
    def __init__(self):
        self.album_tracks = {}
        self.xml_file = Manager

    def get_track(self):
        # Extract tracks with album & artist from xml
        for track_id, track in self.xml_file['Tracks'].items():
            album = track.get('Album')
            artist = track.get('Artist')

            # Ensure the track has both an album and an artist
            if album and artist:
                album_and_artist = (album, artist)

                # Count tracks in all albums //
                if album_and_artist not in self.album_tracks:
                    self.album_tracks[album_and_artist] = 0
                self.album_tracks[album_and_artist] += 1



if __name__ == '__main__':
    # Initialize classes
    mgr = Manager()
    ext = Extract()

    # Manager
    mgr.update_xml_file()
    xml_content = mgr.load_xml()

    # Extract
    ext.xml_file = xml_content
    ext.get_track()