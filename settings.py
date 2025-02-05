import os
import ast
import configparser

from loguru import logger

SETTINGS_FILE = 'settings.ini'


class Settings:
    def __init__(self):
        self.steam_url_id = "mrbean27121"
        self.nick_list = ["Test 1", "Test 2"]
        self.title = "SteamChangeNick"
        self.optimize_nickname = True
        self.chrome_user_data_dir = self.get_chrome_user_data_dir()
        self.load_settings()

    def get_desktop_path(self):
        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
        if not os.path.exists(desktop_dir):
            desktop_dir = os.path.join(os.path.expanduser('~'), 'Рабочий стол')
        return desktop_dir

    def get_chrome_user_data_dir(self):
        # Получаем путь к папке AppData текущего пользователя
        appdata_local_path = os.environ['LOCALAPPDATA']
        chrome_user_data_path = appdata_local_path + fr"\Google\Chrome\User Data {self.title}"
        return chrome_user_data_path

    def get_settings(self):
        return settings.__dict__

    # Функция для обновления настроек
    def update_settings(self, key, value):
        if hasattr(settings, key) and getattr(settings, key) != value:
            setattr(settings, key, value)
            logger.debug(f"Изменено: {key} на {value}")
            settings.save_settings()

    def load_settings(self):
        config = configparser.ConfigParser()
        if not os.path.exists(SETTINGS_FILE):
            self.save_settings()
        else:
            config.read(SETTINGS_FILE, encoding='utf-8')
            for key in self.__dict__:
                if key in config['DEFAULT']:
                    value = config['DEFAULT'][key]
                    try:
                        value = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        # Если значение не может быть интерпретировано, оставляем его как есть
                        pass
                    setattr(self, key, value)
            self.save_settings()

    def save_settings(self):
        config = configparser.ConfigParser()
        for key, value in self.__dict__.items():
            config['DEFAULT'][key] = str(value)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as file:
            config.write(file)


settings = Settings()