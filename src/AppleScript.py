import subprocess
import logging


def run_applescript(script: str) -> None:
    """Run an AppleScript command and return the output."""
    result = subprocess.run(['osascript', '-e', script],
                            capture_output=True,
                            text=True,
                            check=True
                            )
    if result.returncode != 0:
        logging.error(f"AppleScript error: {result.stderr.strip()}")


class AppleScripts:
    def __init__(self, new_playlist_name: str, json_playlist_name: str, album_picked: str, artist_picked: str):
        self.new_playlist_name: str = new_playlist_name
        self.json_playlist_name: str = json_playlist_name
        self.album: str = album_picked
        self.artist: str = artist_picked

    def create_or_clear_playlist(self) -> None:
        """Create a new playlist or clear the existing one."""
        script: str = f'''
        tell application "Music"
            if exists (some playlist whose name is "{self.new_playlist_name}") then
                set existingPlaylist to some playlist whose name is "{self.new_playlist_name}"
                delete every track of existingPlaylist
            else
                set existingPlaylist to (make new playlist with properties {{name:"{self.new_playlist_name}"}})
            end if
        end tell
        '''
        run_applescript(script)

    def add_album_to_playlist(self) -> None:
        """Add tracks from a specific album by an artist to the playlist."""
        script: str = f'''
        tell application "Music"
            set albumTracks to tracks of playlist "Library" whose album is "{self.album}" and artist is "{self.artist}"
            repeat with t in albumTracks
                duplicate t to playlist "{self.new_playlist_name}"
            end repeat
        end tell
        '''
        run_applescript(script)
        logging.info("ADDED TO PLAYLIST:\n      🗂 '%s'", self.new_playlist_name)

    def delete_old_playlist(self) -> None:
        """Delete the old playlist if it exists."""
        script: str = f'''
        tell application "Music"
            if exists (some playlist whose name is "{self.json_playlist_name}") then
                delete (some playlist whose name is "{self.json_playlist_name}")
            end if
        end tell
        '''
        run_applescript(script)
        logging.info("DELETED OLD PLAYLIST:\n      🗑️ '%s'", self.json_playlist_name)

    def rename_playlist(self):
        script: str = f'''
        tell application "Music"
            if exists (some playlist whose name is "{self.json_playlist_name}") then
                set the name of (some playlist whose name is "{self.json_playlist_name}") to "{self.new_playlist_name}"
            end if
        end tell
        '''
        run_applescript(script)
        logging.info("RENAMED PLAYLIST:\n       ℹ️ '%s' to '%s'", self.json_playlist_name,
                     self.new_playlist_name)
