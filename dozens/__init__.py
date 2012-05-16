import json
import urllib
import urllib2


def main():
    user = 'mikamix'
    key = '02e283a5bf8ace2714d9101a171bf5229136d9e4'
    client = Client(user, key)
    client.start()
    print client.get_zones()


class Client(object):

    def __init__(self, user, key):
        self.user = user
        self.key = key

    def start(self):
        url = 'http://dozens.jp/api/authorize.json'
        headers = {'X-Auth-User': self.user, 'X-Auth-Key': self.key}
        response = self.get(url, headers=headers)
        self.token = response.get('auth_token')

    def get_zones(self):
        url = 'http://dozens.jp/api/zone.json'
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.token,
            }
        response = self.get(url, headers=headers)
        return response.get('domain')

    def get(self, url, params={}, headers={}):
        request = urllib2.Request(url + '?' + urllib.urlencode(params))
        for key, value in headers.items():
            request.add_header(key, value)
        response = urllib2.urlopen(request).read()
        return json.loads(response)

if __name__ == '__main__':
    main()
