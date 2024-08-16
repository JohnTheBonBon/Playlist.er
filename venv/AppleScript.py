import subprocess
import logging

class applescripts:
    def __init__(self, playlist_name, JSON_playlist_name, album_picked, artist_picked):
        self.playlist_name = playlist_name
        self.JSON_playlist_name = JSON_playlist_name
        self.album_picked = album_picked
        self.artist_picked = artist_picked

    def run_applescript(self, script):
        """Run an AppleScript command and return the output."""
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"AppleScript error: {result.stderr.strip()}")
            return ""
        return result.stdout.strip()

    def create_or_clear_playlist(self):
        """Create a new playlist or clear the existing one."""
        script = f'''
        tell application "Music"
            if exists (some playlist whose name is "{self.playlist_name}") then
                set existingPlaylist to some playlist whose name is "{self.playlist_name}"
                delete every track of existingPlaylist
            else
                set existingPlaylist to (make new playlist with properties {{name:"{self.playlist_name}"}})
            end if
        end tell
        '''
        self.run_applescript(script)

    def add_album_to_playlist(self):
        """Add tracks from a specific album by an artist to the playlist."""
        script = f'''
        tell application "Music"
            set albumTracks to tracks of playlist "Library" whose album is "{self.album_picked}" and artist is "{self.artist_picked}"
            repeat with t in albumTracks
                duplicate t to playlist "{self.playlist_name}"
            end repeat
        end tell
        '''
        self.run_applescript(script)
        logging.info("ADDED TO PLAYLIST:\n      🗂 '%s'", self.playlist_name)

    def delete_old_playlist(self):
        """Delete the old playlist if it exists."""
        script = f'''
        tell application "Music"
            if exists (some playlist whose name is "{self.JSON_playlist_name}") then
                delete (some playlist whose name is "{self.JSON_playlist_name}")
            end if
        end tell
        '''
        self.run_applescript(script)
        logging.info("DELETED OLD PLAYLIST:\n      🗑️ '%s'", self.JSON_playlist_name)