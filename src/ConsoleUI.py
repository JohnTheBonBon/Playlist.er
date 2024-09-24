from prettytable import PrettyTable
import logging
import aigpy
import sys
import os

from Json import JsonManager
from Playlister import PlaylisterManager
from Xml import XmlManager
from AppleScript import AppleScripts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s >\n %(message)s\n',
                    datefmt='%H:%M:%S', force=True)


class UiFormat:
    @staticmethod
    def table(columns: list[str], rows: list[list[str]]) -> PrettyTable():
        table = PrettyTable()
        table.field_names = columns
        table.align['Function'] = 'l'
        table.align['Value'] = 'l'

        table.field_names = [aigpy.cmd.blue(item) for item in columns]
        for item in rows:
            table.add_row(item)

        return table

    @staticmethod
    def heading(title, table) -> str:
        table_str: str = table.get_string()
        # Gets length of the table from top line
        table_width: int = len(table_str.split()[0])

        padding: str = '-' * ((table_width - len(title) - 2) // 2)
        heading: str = f"{padding} {title} {padding}"
        # If the heading is shorter than the table
        if len(heading) < table_width:
            heading += '-'

        return heading

    @staticmethod
    def message(colour, title, message) -> None:
        title_padding: str = '-' * ((len(message) - len(title) - 2) // 2)
        bottom_padding: str = '-' * len(message)
        heading: str = f"{title_padding} {title} {title_padding}"

        if heading or bottom_padding < message:
            heading += '-'
            bottom_padding += '-'
        print_structure = f"{heading} \n{message} \n{bottom_padding} \n"

        if colour == 'red':
            print(aigpy.cmd.red(print_structure))
        elif colour == 'green':
            print(aigpy.cmd.green(print_structure))

    @staticmethod
    def logo() -> None:
        print('____________________________________________________________________')
        print(r'''
              ___ _             _ _     _               
             / _ \ | __ _ _   _| (_)___| |_    ___ _ __ 
            / /_)/ |/ _` | | | | | / __| __|  / _ \ '__|
           / ___/| | (_| | |_| | | \__ \ |_  |  __/ |   
           \/    |_|\__,_|\__, |_|_|___/\__|  \___|_|   
                          |___/                                                                                                             
        ''')
        print('____________________________________________________________________ \n')


class UiMenu:
    @staticmethod
    def home() -> None:
        UiFormat.logo()
        columns: list = ['Option', 'Function']
        rows: list[list[str]] = [
            ['0', 'Exit'],
            ['1', 'Settings'],
            ['2', 'View Playlist\'er Library'],
            ['\'Name\'', 'Open Playlist\'er']
        ]
        table = UiFormat.table(columns, rows)
        heading = UiFormat.heading('Home Menu', table)
        print(f'{heading} \n{table}')

        UiHandler.home()

    @staticmethod
    def settings() -> None:
        columns: list = ['Option', 'Function', 'Value']
        rows: list[list[[int, str, any]]] = [
            ['0', 'Back'],
            ['1', 'Logging']
        ]

    @staticmethod
    def playlist(playlister_name: str) -> None:
        columns: list = ['Option', 'Function']
        rows: list[list[str]] = [
            ['0', 'Back'],
            ['1', 'Run'],
            ['2', 'Edit'],
            ['3', 'Delete']
        ]
        table = UiFormat.table(columns, rows)
        heading = UiFormat.heading('Playlist', table)
        print(f'{heading} \n{table}')
        print(f'>>> {aigpy.cmd.blue(playlister_name)}')

        UiHandler.playlist(playlister_name)

    @staticmethod
    def config(config_list: dict, playlister_name: str) -> None:
        columns: list = ['Option', 'Function', 'Value']
        rows: list[list[[int, str, any]]] = [['0', 'Back', '...']]
        rows += [
            [index + 1, param, aigpy.cmd.yellow(value)]
            # Iterate over both params and values with their position (index)
            for index, (param, value) in enumerate(config_list.items())
        ]
        table = UiFormat.table(columns, rows)
        heading = UiFormat.heading('Configuration', table)
        print(f'{heading} \n{table}')
        print(f'>>> {aigpy.cmd.blue(playlister_name)}')

        UiHandler.config(playlister_name, config_list, rows)

    @staticmethod
    def all_playlists(available_playlists: list) -> None:
        columns: list = ['All Playlists']
        rows: list = [[playlist] for playlist in available_playlists]
        table = UiFormat.table(columns, rows)
        print(table)

        columns: list = ['Option', 'Function']
        rows: list = [
            ['0',       'Back'],
            ['1',       'Run All'],
            ['\'Name\'',    'Open Playlist']
        ]
        table = UiFormat.table(columns, rows)
        print(table)

        UiHandler.all_playlists(available_playlists)

    @staticmethod
    def input(text) -> str:
        if text:
            print(f'\n---- {text} -----')
            user_input: str = input(aigpy.cmd.yellow('Option & Value: '))
        else:
            print('\n---- Enter Option ----')
            user_input: str = input(aigpy.cmd.yellow('Option: '))
        print()

        return user_input


class UiHandler:
    @staticmethod
    def home() -> None:
        user_input: str = UiMenu.input('')

        match user_input:
            case '0':
                sys.exit(0)
            case '1':
                UiMenu.settings()
            case '2':
                UiFunctions('').view_playlists()
            case _:
                if user_input.isdigit():
                    UiFormat.message('red', 'Invalid Entry', 'Please enter a valid number from the '
                                                             'table below.')
                    UiMenu.home()
                else:
                    if not UiFunctions(user_input).find_playlist():
                        UiMenu.home()

    @staticmethod
    def playlist(playlister_name) -> None:
        user_input: str = UiMenu.input(None)

        match user_input:
            case '0':
                UiMenu.home()
            case '1':
                UiFunctions(playlister_name).run()
            case '2':
                UiFunctions(playlister_name).get_config()
            case '3':
                ...
            case _:
                UiFormat.message('red', 'Invalid Entry', 'Please enter a valid number from the table'
                                                         ' below.')
                UiMenu.playlist(playlister_name)

    @staticmethod
    def all_playlists(available_playlists) -> None:
        user_input: str = UiMenu.input('')

        match user_input:
            case '0':
                UiMenu.home()
            case '1':
                print('should run all playlists')
            case _:
                if user_input.isdigit():
                    UiFormat.message('red', 'Invalid Entry', 'Please enter a valid number from the '
                                                             'table below.')
                    UiMenu.all_playlists(available_playlists)
                else:
                    if not UiFunctions(user_input).find_playlist():
                        UiMenu.all_playlists(available_playlists)

    @staticmethod
    def config(playlister_name, config_list, rows) -> None:
        user_input: str = UiMenu.input(f'Enter Option & Value {aigpy.cmd.green('(Eg: 4 true)')}')

        if user_input == '0':
            UiMenu.playlist(playlister_name)
            return

        try:
            option, value = user_input.split(maxsplit=1)  # [2, true]
            option: int = int(option)

            if 0 < option < len(rows):
                param = rows[option][1]
                val_type = type(config_list[param])

                converted_val = UiFunctions.config_type_convertion(value, val_type)
                if converted_val is not None:
                    UiFunctions(playlister_name).update_json(param, converted_val)
                    UiFormat.message('green', 'Success', f'{playlister_name} config updated')
                    UiFunctions(playlister_name).get_config()
                else:
                    UiFormat.message('red', 'Invalid Value', 'Please enter a valid Value related '
                                                             'to its Function from the config table. ')

        except ValueError:
            UiFormat.message('red', 'Invalid Option', 'Please enter a valid Option & Value from '
                                                      'the config table.')
        UiMenu.config(config_list, playlister_name)


class UiFunctions:
    def __init__(self, playlister_name):
        self.playlister_name: str = playlister_name.lower()
        self.playlist_folder: str = '../data/Playlist\'er library'

        if playlister_name:
            self.xml_manager = XmlManager()
            self.json_manager = JsonManager(self.playlister_name)
            self.playlister_manager = PlaylisterManager(self.playlister_name)

            self.json_load = self.json_manager.load()

    def view_playlists(self) -> None:
        if os.path.exists(self.playlist_folder):
            available_playlists: list = [
                os.path.splitext(file)[0] for file in os.listdir(self.playlist_folder)
                if file.endswith('.json')
            ]
            UiMenu.all_playlists(available_playlists)
        else:
            UiFormat.message('red', 'Library Empty', 'Your Playlist\'er library is empty')
            UiMenu.home()

    def find_playlist(self) -> None:
        folder_dir: str = os.path.join(self.playlist_folder, '')
        playlist_exists: bool = os.path.exists(folder_dir + self.playlister_name + '.json')

        if playlist_exists:
            UiMenu.playlist(self.playlister_name)
            UiMenu.input('')
        else:
            UiFormat.message('red', 'Invalid Entry', 'Playlist not found!, Please enter a valid '
                                                     'playlist.')

    def get_config(self) -> None:
        try:
            config_list = self.json_load['Config']
            UiMenu.config(config_list, self.playlister_name)
        except ValueError as error:
            print(f'Error occurred... {error}')

    @staticmethod
    def config_type_convertion(value, val_type):
        if val_type == bool:
            if value.lower() in ['true', 'false']:
                return value.lower() == 'true'
        elif val_type == int:
            if value.isdigit():
                return int(value)
        elif val_type == str:
            return str(value)
        else:
            return None

    def update_json(self, param, converted_val):

        if param == 'Playlist name':
            old_playlist_name = self.json_load['Config'].get('Playlist name')
            apple = AppleScripts(converted_val, old_playlist_name, '', '')
            apple.rename_playlist()

        self.json_load['Config'][param] = converted_val
        self.json_manager.save(self.json_load)

    def run(self) -> None:
        try:
            self.json_manager.load()
            self.xml_manager.refresh_file()
            self.playlister_manager.create()
            UiFormat.message('green', 'Success', f'{self.playlister_name} playlist created')
        except ValueError as error:
            UiFormat.message('red', 'Error Occurred', f"{error}")

        UiMenu.home()


if __name__ == '__main__':
    UiMenu.home()
