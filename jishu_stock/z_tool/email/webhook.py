import requests



webhook_url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
# webhook_url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b03afced-5adf-4b8a-b781-8710c5824463'
headers = {
    'Content-Type': 'application/json',
}

params = {
    # 'key': '98a913b1-0c05-4865-ade0-8272bd9586f1',
    'key': 'b03afced-5adf-4b8a-b781-8710c5824463',
}



def getJsonData(content):
    json_data = {
        'msgtype': 'text',
        'text': {
            'content':  content,
            # 'mentioned_list':['@all']
        },
    }
    return json_data


def sendData(content):

   requests.post(webhook_url, params=params, headers=headers, json=getJsonData(content))

if __name__ == '__main__':
    sendData("wangweicheng")