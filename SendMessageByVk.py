import requests
import random
from info import token, version
def sendMsg(userid, msg):
    requests.post('https://api.vk.com/method/messages.send',
                                                params={
                                                    'random_id': random.randrange(1, 21567),
                                                    'peer_id': userid,
                                                    'message': msg,
                                                    'access_token': token,
                                                    'v': version,
                                                }
                                                ).json()
    print(msg)