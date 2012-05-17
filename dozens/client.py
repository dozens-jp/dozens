import json
import urllib
import urllib2
from .models import Zone
from .models import Record
from .exceptions import DozensException


class Client(object):

    AUTHORIZE_URL = 'http://dozens.jp/api/authorize.json'
    GET_ZONES_URL = 'http://dozens.jp/api/zone.json'
    ADD_ZONE_URL = 'http://dozens.jp/api/zone/create.json'
    DELETE_ZONE_URL = 'http://dozens.jp/api/zone/delete/%s.json'

    GET_RECORDS_URL = 'http://dozens.jp/api/record/%s.json'
    ADD_RECORD_URL = 'http://dozens.jp/api/record/create.json'
    UPDATE_RECORD_URL = 'http://dozens.jp/api/record/update/%d.json'
    DELETE_RECORD_URL = 'http://dozens.jp/api/record/delete/%d.json'

    def __init__(self, user, key):
        self.user = user
        self.key = key

    def start(self):
        headers = {
            'X-Auth-User': self.user,
            'X-Auth-Key': self.key,
            }
        response = self._do_request(self.AUTHORIZE_URL, headers=headers)
        self.token = response.get('auth_token')

    def get_zones(self):
        zones = self.get(self.GET_ZONES_URL).get('domain')
        return [Zone(int(zone.get('id')), zone.get('name')) for zone in zones]

    def add_zone(self, name, add_google_apps=False, google_authorize=None):
        params = {
            'name': name,
            'add_google_apps': add_google_apps,
            'google_authorize': google_authorize
            }
        zones = self.post(self.ADD_ZONES_URL, params).get('domain')
        for zone in zones:
            if zone.get('name') == name:
                return Zone(zone.get('id'), zone.get('name'))

    def delete_zone(self, zone_id):
        self.delete(self.DELETE_ZONES_URL % zone_id)

    def get_records(self, zone_name):
        records = self.get(self.GET_RECORDS_URL % zone_name).get('record')
        return [Record(int(record.get('id')),
                       record.get('name'),
                       record.get('type'),
                       record.get('prio'),
                       record.get('content'),
                       int(record.get('ttl'))) for record in records]

    def add_record(self,
                   zone_name,
                   record_name,
                   record_type,
                   priority,
                   content,
                   ttl=7200):
        params = {
            'domain': zone_name,
            'name': record_name,
            'type': record_type,
            'prio': priority,
            'content': content,
            'ttl': ttl,
            }
        records = self.post(self.ADD_RECORD_URL, params).get('record')
        for record in records:
            if record.get('content') == content:
                return Record(int(record.get('id')),
                              record.get('name'),
                              record.get('type'),
                              record.get('prio'),
                              record.get('content'),
                              int(record.get('ttl')))

    def update_record(self, record_id, priority=None, content=None, ttl=None):
        params = {}
        if priority:
            params['prio'] = priority
        if content:
            params['content'] = content
        if ttl:
            params['ttl'] = ttl
        records = self.post(self.UPDATE_RECORD_URL % record_id, params)
        for record in records:
            if int(record.get('id')) == record_id:
                return Record(record_id,
                              record.get('name'),
                              record.get('type'),
                              record.get('prio'),
                              record.get('content'),
                              int(record.get('ttl')))

    def delete_record(self, record_id):
        self.delete(self.DELETE_RECORD_URL % record_id)

    def get(self, url, params={}):
        if params:
            url = url + '?' + urllib.urlencode(params)
        return self._do_api_request(url)

    def post(self, url, params={}):
        return self._do_api_request(url, params)

    def delete(self, url, params={}):
        return self._do_api_request(url, params, 'DELETE')

    def _do_api_request(self, url, data={}, method=None):
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.token,
            }
        return self._do_request(url, data, headers, method)

    def _do_request(self, url, data={}, headers={}, method=None):
        request = urllib2.Request(url)
        if method:
            request.get_method = lambda: method
        if data:
            request.add_data(data)
        for key, value in headers.items():
            request.add_header(key, value)

        response = urllib2.urlopen(request)
        if response.code == 200:
            return json.loads(response.read())
        else:
            raise DozensException(response.code)