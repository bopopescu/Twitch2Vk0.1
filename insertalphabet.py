import string
import mysql.connector
print(string.digits)
config = {
    'host': "remotemysql.com",
    'user': "a0Pv8eJGfa",
    'passwd': "L6EW1UIcgi",
    'database': 'a0Pv8eJGfa'
}
mydb = mysql.connector.connect(**config)
mycursor = mydb.cursor()
for letter in list(string.digits):
    print(letter)
    sql = "INSERT INTO users (VKID, TwitchUser, LetIndex) VALUES (%s, %s,%s)"
    val = (0, 'blank', letter)
    mycursor.execute(sql,val)
    mydb.commit()
