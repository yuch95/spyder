import json

import requests

base_url = 'http://www.jiangroom.com/queryRoomsAsync?offset={}'
dataNum = 5328
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Safari/537.36',
}


class JingRoom:
    roomData = []

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(headers)

    def get_data(self, num):
        print(num)
        return self.session.get(base_url.format(num)).json()

    def main(self):
        for i in range(0, dataNum + 1, 12):
            self.roomData += self.get_data(i)
        with open('./source_data/room.json', 'w') as r:
            json.dump(self.roomData, r, ensure_ascii=False)


if __name__ == '__main__':
    JingRoom().main()
