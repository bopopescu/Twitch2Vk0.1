import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import mysql.connector
from SendMessageByVk import sendMsg
from info import *


mydb = mysql.connector.connect(**config)
SelectCursor = mydb.cursor()



lastlinkInSQL = eval(open('lastLinkTxt.txt', 'r').read())

while True:
    time.sleep(300)
    lastPickedLink = eval(open('lastLinkTxt.txt', 'r').read())

    if mydb.is_connected() == False:
        print('mysql reconnect')
        try:
            mydb.ping(reconnect=True, attempts=3, delay=5)
        except mysql.connector.Error as err:
            mydb = mysql.connector.connect(**config)
            SelectCursor = mydb.cursor()
            SelectCursor.execute('SELECT subLink, idLinkSub FROM linksToSub ORDER BY idLinkSub DESC LIMIT 1')
            lastlinkInSQL = SelectCursor.fetchone()
            mydb = mysql.connector.connect(**config)



    SelectCursor = mydb.cursor()
    SelectCursor.execute('SELECT subLink, idLinkSub FROM linksToSub ORDER BY idLinkSub DESC LIMIT 1')
    lastlinkInSQL = SelectCursor.fetchone()

    print(lastlinkInSQL)


    if lastPickedLink[1] != lastlinkInSQL[1]:

        pickedcurs = mydb.cursor()
        pickedcurs.execute('SELECT subLink, idLinkSub FROM linksToSub ORDER BY idLinkSub DESC LIMIT %s' % ((int(lastlinkInSQL[1])+1) - int(lastPickedLink[1])))
        inLimGot = pickedcurs.fetchall()
        print(int(lastPickedLink[1]), int(lastlinkInSQL[1]))
        for k in range(((int(lastlinkInSQL[1])+1) - int(lastPickedLink[1]))):
            print(k)
            link = str(inLimGot[k][0])





            chrome_options = Options()
            # chrome_options.add_argument("--user-data-dir=chrome-data")
            chrome_options.add_argument("--headless")


            driver = webdriver.Chrome('/usr/local/bin/chromedriver',    #  C:\\Users\\Nickli1\\PycharmProjects\\untitled\\chromedriver_win32\\chromedriver.exe | /usr/local/bin/chromedriver
                                      options=chrome_options)
            driver.get('https://twitch.tv')
            print('Opened Browser')
            try:
                cookies = pickle.load(open("cookies.pkl", "rb"))
                for cookie in cookies:
                    if 'expiry' in cookie:
                        del cookie['expiry']
                    driver.add_cookie(cookie)
            except:
                pass
            driver.get(link)  # Already authenticated
            avatarBruh ='/html/body/div[1]/div/div[2]/nav/div/div[3]/div[6]/div/div/div/div[1]/button/div/figure/img'
            xpathFollow = "/html/body/div[1]/div/div[2]/div/main/div[1]/div/div[2]/div/div[1]/div[3]/div[1]/div/div/div[1]/div/div/div/div/button"
            loginButton = '/html/body/div[1]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button'
            time.sleep(10)

            try:
                if driver.find_element_by_xpath(avatarBruh).get_attribute('src') == 'https://static-cdn.jtvnw.net/jtv_user_pictures/afc3bf15-4690-4eed-b231-34b224adf1d6-profile_image-70x70.png':
                    if driver.find_element_by_xpath(xpathFollow).get_attribute('data-a-target') == 'follow-button':
                        try:
                            driver.find_element_by_xpath(xpathFollow).click()
                            time.sleep(3)
                            print('Готово')
                        except:
                            print('Кнопка не нажалась')
                            sendMsg(Admin_id, 'Кнопка не нажимается. Сюда: '+ link)
                    else:
                        sendMsg(Admin_id, 'Что то не то. Проверить на наличие подписки: ' + link)
                        print('Ой, уже подписаны на твиче. Готово!')
                driver.quit()
            except:
                try:
                    if driver.find_element_by_xpath(loginButton).get_attribute('data-a-target') == 'login-button':
                        sendMsg(Admin_id, 'Куки слетели. Подписаться: ' + link)
                        print('Что-то с ботом')
                except:
                    sendMsg(Admin_id, 'Канал не существует или куки слетели. Сюда: ' + link)
                    print('Такого канала несуществует, повторите попытку.\n(или что то с ботом, админ уже проверяет)')
                driver.get_screenshot_as_file('error {}.png'.format(time.strftime("%Y%m%d-%H%M%S")))
                driver.quit()
        open('lastLinkTxt.txt', 'w').write(str(lastlinkInSQL))
        SelectCursor.close()
        mydb.close()

    else:
        SelectCursor.close()
        mydb.close()







