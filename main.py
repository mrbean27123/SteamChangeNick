import time
import random
import ctypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import settings
from byteChecker import replace_russian_with_english

if __name__ == "__main__":
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--headless=new")
    driver_options.add_argument('--user-data-dir=' + settings.chrome_user_data_dir)
    driver_options.add_argument('--profile-directory=Profile ' + settings.title)
    with webdriver.Chrome(options=driver_options) as driver:
        url_edit = f"https://steamcommunity.com/id/{settings.steam_url_id}/edit/info"
        driver.get(url_edit)
        # Если не авторизован
        if "login" in driver.current_url:
            driver.close()
            driver_options = webdriver.ChromeOptions()
            driver_options.add_argument('--user-data-dir=' + settings.chrome_user_data_dir)
            driver_options.add_argument('--profile-directory=Profile ' + settings.title)
            with webdriver.Chrome(options=driver_options) as driver:
                url_edit = f"https://steamcommunity.com/id/{settings.steam_url_id}/edit/info"
                driver.get(url_edit)
                ctypes.windll.user32.MessageBoxW(0, "Вы не авторизованы в Steam!", settings.title, 16)
            exit()

        # Ждём пока будет элемент с ником
        input_nick = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[contains(@class, "DialogInput DialogInputPlaceholder DialogTextInputBase Focusable")]')))
        input_nick_text = input_nick.get_attribute("value")
        input_nick.clear()

        # Исключаем старое имя из списка
        nick_list = settings.nick_list
        if input_nick_text in nick_list:
            nick_list.remove(input_nick_text)
        random_nick = random.choice(nick_list)
        if settings.optimize_nickname is True:
            random_nick_replace = replace_russian_with_english(random_nick)
        else:
            random_nick_replace = random_nick
        input_nick.send_keys(random_nick_replace)

        button_change = driver.find_element(By.XPATH, '//button[contains(@class, "DialogButton _DialogLayout Primary Focusable")]')
        button_change.click()

        # Очищаю историю ников
        driver.execute_script("ShowClearAliasDialog()")

        # Ждём пока будет элемент подтверждения
        button_span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "btn_green_steamui btn_medium")]')))
        time.sleep(0.5)
        button_span.click()
