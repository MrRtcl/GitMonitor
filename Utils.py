import Config
import requests
import json

class Repo:
    def __init__(self, name, url, description='', keyword='default'):
        self.name = name
        self.url = url
        self.description = description
        self.keyword = keyword

    def __str__(self):
        return f'Keyword: {self.keyword}\n[{self.name}]({self.url}): \n{self.description}\n'

    def __repr__(self):
        return f'Repo({self.name!r}, {self.url!r})'
    
    def __eq__(self, other):
        return self.url == other.url
    

def ServerChan(msg):
    # sckey为自己的server SCKEY
    sckey = Config.SERVER_CHAN_KEY
    url = 'https://sc.ftqq.com/'+sckey+'.send?text=GitHub&desp='+msg
    requests.get(
        url,
        headers=Config.HEADERS,
        proxies=Config.PROXY,
        timeout=Config.TIMEOUT,
        verify=False
    )

def WXWork(msg):
    data = json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "content": msg
            }
        })
    # 指定机器人发送消息
    resp = requests.post(Config.WXURL,data,auth=('Content-Type', 'application/json'))
    return resp.json()



