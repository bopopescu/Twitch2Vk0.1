import imaplib
import email.message
import mysql.connector
from SendMessageByVk import *
from bs4 import BeautifulSoup
from info import mypass, config, Admin_id


checkhtml = 1
mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login('twitch2vk@mail.ru', mypass)
past_email_uid = open('lastEmailUid.txt', 'r')
while True:  # Постоянная проверка новых писем на наличие изменений, нужно поменять на проверку переменной для исключения возможности порчи ssd из-за постоянной перезаписи файла
    try:
        mail.list()
        mail.select('inbox')

        result, data = mail.uid('search', None, "ALL")  # Выполняет поиск и возвращает UID писем.
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        msg_raw = data[0][1]
        msg = email.message_from_bytes(msg_raw)
        if msg.is_multipart() == True:
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    txt = part.get_payload(decode=True).decode()
        else:
            txt = msg.get_payload(decode=True).decode()
        if checkhtml != txt:
            checkhtml = txt

            # Извлечение из полученного письма юзернейма стримера и преобразование его юзернейма в ссылку, нужно изменить на вытаскивание готовой ссылки, ведь могут быть проблемы с другими кодировками юзернеймов
            soup = BeautifulSoup(txt, "html.parser")
            info = []
            for a in soup.find_all('a', href=True, style='color:#999'):
                link = str(a.text)
                print(link)
            if link.split('/')[2] == 'www.twitch.tv':
                link = 'https://twitch.tv/' + link.split('/')[3]
                try:
                    mydb = mysql.connector.connect(**config)
                    mycursor = mydb.cursor()
                    mycursor.execute('SELECT * FROM users')
                    myresult = mycursor.fetchall()
                    username = link.split('/')[3]
                    if latest_email_uid != bytes(past_email_uid):  # Проверка на изменение имени пользователя
                        past_email_uid = open('lastEmailUid.txt', 'w').write(str(latest_email_uid))
                        for x in myresult:
                            if x[1] == link.lower():
                                print(x)
                                link_for_user = '👁 Пользователь {} начал свою трансляцию. 👁 Ссылка:\n{}'.format(username, link)
                                sendMsg(x[0], link_for_user)
                    mycursor.close()
                    mydb.disconnect()
                except:
                    pass
    except:
        print('Something wrong')
        sendMsg(Admin_id, 'Что-то с почтой')
        mail = imaplib.IMAP4_SSL('imap.mail.ru')
        mail.login('twitch2vk@mail.ru', mypass)
        past_email_uid = open('lastEmailUid.txt', 'r')
        pass
