from selenium import webdriver
from SeleniumCookies import cookie_injector

driver = webdriver.Chrome('C:\\Users\\Nickli1\\PycharmProjects\\untitled\\chromedriver_win32\\chromedriver.exe')
driver.get("https://www.google.com")

#COOKIE INJECTION
cookies = cookie_injector.inject_cookie()
for cookie in cookies:
	try:
		driver.add_cookie(cookie)
	except:
		pass