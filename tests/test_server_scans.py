import cloudpassage
import pytest
import sys
import os
import datetime
from dateutil.parser import parse
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'lib'))
from api_controller import ApiController


class TestServerScans:
    def build_api_object(self):
        return ApiController()

    def build_test_date(self, day):
        return (datetime.datetime.now() - datetime.timedelta(days=day)).strftime("%Y-%m-%d")

    def normalize_date(self, date):
        return parse(date).strftime("%Y-%m-%d")

    def test_scan_filter_by_since(self):
        api = self.build_api_object()
        ten_days_ago = self.build_test_date(10)
        resp = api.get('/v1/scans?since=%s' % ten_days_ago)
        assert resp['scans']

        for scan in resp['scans']:
            assert self.normalize_date(scan['created_at']) >= ten_days_ago

    def test_scan_filter_by_until(self):
        api = self.build_api_object()
        ten_days_ago = self.build_test_date(10)
        resp = api.get('/v1/scans?until=%s' % ten_days_ago)
        assert resp['scans']

        for scan in resp['scans']:
            assert self.normalize_date(scan['created_at']) <= ten_days_ago

    def test_scan_filter_by_server(self):
        api = self.build_api_object()
        servers = api.get('/v1/servers')
        assert servers['servers']

        server_id = servers['servers'][0]['id']
        resp = api.get('/v1/scans?server_id=%s' % server_id)
        assert resp['scans']

        for scan in resp['scans']:
            assert scan['server_id'] == server_id
