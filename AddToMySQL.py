from SendMessageByVk import *
import mysql.connector
from info import *
import traceback

mydb = mysql.connector.connect(**config)
mycursor = mydb.cursor()
def getBruh(id):
    response = requests.get('https://api.vk.com/method/messages.getHistory',
                            params={
                                'peer_id': id,
                                'access_token': token,
                                'v': version,
                            }
                            )
    try:
        data = response.json()['response']['items']
        return data
    except:
        pass



def addToMySql_vkid_link(bruhId, link):
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (VKID, TwitchUser, LetIndex) VALUES (%s, %s, %s)"
    val = (bruhId, link, link[19])
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount == -1:
        sendMsg(bruhId, 'Неудалось добавить в базу данных. Попробуйте еще разок')
    else:
        sendMsg(bruhId, 'Стример ' + TwitchName + ' добавлен в базу данных')
    print(mycursor.rowcount, "record inserted.")

def deleteFromMySql_vkid_link(bruhId, link):
    sql = "DELETE FROM users WHERE VKID = %s and TwitchUser= %s"
    val = (bruhId, link)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount == -1:
        sendMsg(bruhId, 'Нет в базе данных')
    else:
        sendMsg(bruhId, 'Стример ' + TwitchName + ' удален из базы данных')
    print(mycursor.rowcount, "record deleted.")
def Error():
    sendMsg(id, 'Команда не распознана. Повторите все заново.\n(Если не получается напишите админу)')




while True:    # LongPoll получение последнего сообщения по peer_id пользователя

    try:
        if mydb.is_connected() == False:
            sendMsg(id, 'problem mysql')
            try:
                mydb.ping(reconnect=True, attempts=3, delay=5)
            except mysql.connector.Error as err:
                mydb = mysql.connector.connect(**config)
                mycursor = mydb.cursor()
                mydb = mysql.connector.connect(**config)


        getServer = requests.get('https://api.vk.com/method/groups.getLongPollServer',   # Подключаем long poll проверку
                                 params={
                                     'group_id': Group_id,
                                     'access_token': token,
                                     'v': version
                                 }
                                 )
        var1 = getServer.json()['response']

        check = requests.get(    # Получаем id пользователя написавшего последнее сообщение (тут можно и узнать что он написал, но это довольно сложно, поэтому я использую другой метод)
            '{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=2'.format(server=var1['server'], key=var1['key'],
                                                                                     ts=var1['ts'])).json()
        updates = check['updates']
        if updates:
            for element in updates:
                var1['ts'] = check['ts']
        el1 = str(updates).split(" ")
        try:
            id = (''.join(list(el1[13][:-1])))
        except:
            id = 1
            print("Waiting for message")
    except:
        print(token)
        print('problemVkConnection')
        pass

    while id != 1: # Впихиваем последнее сообщение пользователя в базу данных, сейчас нужно поменять на проверку наличия ссылки на твич для того что бы впихать
        try:
            workingLink = None
            LastUserMsg = getBruh(id)[0]['text']
            print("Message", LastUserMsg, 'from', id)

            if LastUserMsg.split(' ')[0].lower() == 'отписка':
                workingLink = 'https://twitch.tv/' + LastUserMsg.split(' ')[1]
                TwitchName = LastUserMsg.split(' ')[1].lower()
                deleteFromMySql_vkid_link(id, workingLink)
                id = 1
            elif LastUserMsg.lower() == 'отключиться от рассылки':
                mycursor = mydb.cursor()
                deleteAll = 'DELETE FROM users WHERE VKID=%s' % id
                mycursor.execute(deleteAll)
                print(mycursor.rowcount, "record deleted.")
                sendMsg(id, 'Вы отписались от всех рассылок')
                mydb.commit()
                id = 1
            elif LastUserMsg.lower() == 'меню':
                sendMsg(id, '1. Подписка *никнэйм стримера*"\n\n2. Отписка *никнэйм стримера*\n\n3. Отключиться от рассылки\n\n4.*ссылка*')
                id = 1
            elif LastUserMsg.split(' ')[0].lower() == 'подписка':
                workingLink = 'https://twitch.tv/' + LastUserMsg.split(' ')[1].lower()
                TwitchName = LastUserMsg.split(' ')[1].lower()
                print(workingLink)
                addToMySql_vkid_link(id, workingLink)
                mycursor = mydb.cursor()
                mydb.cursor().execute('INSERT INTO linksToSub (subLink) VALUES ("%s")' % workingLink)
                mydb.commit()
                id = 1

            else:

                LinkSeparated = LastUserMsg.split('/')

                for i in range(len(LinkSeparated)):

                    if LinkSeparated[i] == 'twitch.tv' or LinkSeparated[i] == 'www.twitch.tv' or LinkSeparated[i] == 'm.twitch.tv':
                        if i == 2:
                            workingLink = 'https://twitch.tv/' + LinkSeparated[i + 1].lower()
                            TwitchName = LinkSeparated[i + 1].lower()
                            try:
                                workingLink = workingLink.split('?')[0]
                                TwitchName = TwitchName.split('?')[0]
                            except:
                                pass
                            print(workingLink)
                            TwitchNameFL = tuple(LinkSeparated[i + 1][0])
                            addToMySql_vkid_link(id, workingLink)
                            mycursor = mydb.cursor()
                            mydb.cursor().execute('INSERT INTO linksToSub (subLink) VALUES ("%s")' % workingLink)
                            mydb.commit()
                            id = 1
                        else:
                            Error()
                            id = 1
                    elif len(LinkSeparated) - 1 == i and type(workingLink) != str:
                                Error()
                                id = 1


        except Exception:
            traceback.print_exc()
            Error()
            id = 1





