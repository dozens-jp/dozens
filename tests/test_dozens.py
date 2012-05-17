import json
import dozens
import urllib2
import mock
from StringIO import StringIO
from unittest import TestCase


class DozensTestCase(TestCase):

    def test_start(self):
        with mock.patch('dozens.urllib2.urlopen') as m:
            m.return_value = self.mock_response({'auth_token': 'dummy_token'})

            testee = dozens.Dozens('user', 'key')
            testee.start()
            self.assertEqual(testee.token, 'dummy_token')

            request = m.call_args[0][0]
            self.assertEqual(request.get_full_url(), testee.AUTHORIZE_URL)
            self.assertEqual(request.get_header('X-auth-user'), 'user')
            self.assertEqual(request.get_header('X-auth-key'), 'key')
            self.assertEqual(request.get_method(), 'GET')

    def test_get_zones(self):
        with mock.patch('dozens.urllib2.urlopen') as m:
            dummy = [
                {'id': 1, 'name': 'name1'},
                {'id': 2, 'name': 'name2'},
                ]
            m.return_value = self.mock_response({'domain': dummy})

            testee = dozens.Dozens('user', 'key')
            testee.token = 'token'

            zones = testee.get_zones()
            self.assertEqual(zones[0].id, 1)
            self.assertEqual(zones[0].name, 'name1')
            self.assertEqual(zones[1].id, 2)
            self.assertEqual(zones[1].name, 'name2')

            request = m.call_args[0][0]
            self.assertEqual(request.get_full_url(),
                             testee.GET_ZONES_URL)
            self.assertEqual(request.get_header('Content-type'),
                             'application/json')
            self.assertEqual(request.get_header('X-auth-token'),
                             'token')
            self.assertEqual(request.get_method(), 'GET')

    def test_add_zone(self):
        with mock.patch('dozens.urllib2.urlopen') as m:
            dummy = [
                {'id': 1, 'name': 'name1'},
                {'id': 2, 'name': 'name2'},
                ]
            m.return_value = self.mock_response({'domain': dummy})

            testee = dozens.Dozens('user', 'key')
            testee.token = 'token'

            zone = testee.add_zone('name2', True, 'google')
            self.assertEqual(zone.id, 2)
            self.assertEqual(zone.name, 'name2')

            request = m.call_args[0][0]
            self.assertEqual(request.get_full_url(),
                             testee.ADD_ZONE_URL)
            self.assertEqual(request.get_header('Content-type'),
                             'application/json')
            self.assertEqual(request.get_header('X-auth-token'),
                             'token')
            self.assertEqual(request.get_method(), 'POST')
            self.assertEqual(request.data['name'], 'name2')
            self.assertTrue(request.data['add_google_apps'])
            self.assertEqual(request.data['google_authorize'], 'google')

    def test_delete_zone(self):
        with mock.patch('dozens.urllib2.urlopen') as m:
            m.return_value = self.mock_response({})

            testee = dozens.Dozens('user', 'key')
            testee.token = 'token'
            testee.delete_zone(1)

            request = m.call_args[0][0]
            self.assertEqual(request.get_full_url(),
                             testee.DELETE_ZONE_URL % 1)
            self.assertEqual(request.get_header('Content-type'),
                             'application/json')
            self.assertEqual(request.get_header('X-auth-token'),
                             'token')
            self.assertEqual(request.get_method(), 'DELETE')

    def test_get_records(self):
        with mock.patch('dozens.urllib2.urlopen') as m:
            dummy = [
                {'id': 1,
                 'name': 'name1',
                 'type': 'type1',
                 'prio': 'prio1',
                 'content': 'content1',
                 'ttl': 7200},
                {'id': 2,
                 'name': 'name2',
                 'type': 'type2',
                 'prio': 'prio2',
                 'content': 'content2',
                 'ttl': 7200},
                ]
            m.return_value = self.mock_response({'record': dummy})

            testee = dozens.Dozens('user', 'key')
            testee.token = 'token'
            records = testee.get_records('domain')
            self.assertEqual(records[0].id, 1)
            self.assertEqual(records[0].name, 'name1')
            self.assertEqual(records[0].type, 'type1')
            self.assertEqual(records[0].priority, 'prio1')
            self.assertEqual(records[0].content, 'content1')
            self.assertEqual(records[0].ttl, 7200)

            self.assertEqual(records[1].id, 2)
            self.assertEqual(records[1].name, 'name2')
            self.assertEqual(records[1].type, 'type2')
            self.assertEqual(records[1].priority, 'prio2')
            self.assertEqual(records[1].content, 'content2')
            self.assertEqual(records[1].ttl, 7200)

            request = m.call_args[0][0]
            self.assertEqual(request.get_full_url(),
                             testee.GET_RECORDS_URL % 'domain')
            self.assertEqual(request.get_header('Content-type'),
                             'application/json')
            self.assertEqual(request.get_header('X-auth-token'),
                             'token')
            self.assertEqual(request.get_method(), 'GET')

    def mock_response(self, value):
        body = StringIO(json.dumps(value))
        response = urllib2.addinfourl(body, {}, 'dummy_url')
        response.code = 200
        return response
