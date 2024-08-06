from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
#from datetime import datetime, timezone, timedelta
#import time
import telepot
import os

TG_TOK = os.getenv('TG_TOK')
CHAT_ID = os.getenv('CHAT_ID')

class Cerca:
    tasso = None

    def rileva_str(self):
        chrome_options = Options()
        options = [
            "enable-automation",
            "--headless",
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        for option in options:
            chrome_options.add_argument(option)

        driver = webdriver.Chrome(
        service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=chrome_options
        )

        driver.implicitly_wait(6)
        driver.get('https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/index.en.html')
        self.tasso = float(driver.find_element(By.XPATH, '//*[@id="main-wrapper"]/main/div[3]/div[2]/table/tbody/tr[1]/td/strong').text) + 0.085
        self.tasso = '{:.3f}'.format(self.tasso).rstrip('0').rstrip('.')



    def manda_mess(self):
        if self.tasso is not None:
            bot = telepot.Bot(TG_TOK)
            messaggio = 'Tasso <a href="https://www.justetf.com/it/etf-profile.html?isin=LU0290358497#panoramica">XEON</a> di oggi: ' + str(self.tasso)
            bot.sendMessage(CHAT_ID, messaggio, parse_mode='HTML')
        else:
            print("Tasso is None, cannot send message.")

    def __init__(self):
        print('Avvio init')

cerca_instance = Cerca()

# Richiama i metodi separatamente
cerca_instance.rileva_str()
cerca_instance.manda_mess()
