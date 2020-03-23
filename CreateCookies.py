import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle

chrome_options = Options() # Запись кукизов раз в месяц
# chrome_options.add_argument("--user-data-dir=chrome-data")

driver = webdriver.Chrome('C:\\Users\\Nickli1\\PycharmProjects\\untitled\\chromedriver_win32\\chromedriver.exe',options=chrome_options)

# chrome_options.add_argument("user-data-dir=chrome-data")
driver.get('https://twitch.tv')
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']
    driver.add_cookie(cookie)
driver.get('https://twitch.tv/dawgdebik')
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
time.sleep(15)  # Time to enter credentials
driver.quit()

