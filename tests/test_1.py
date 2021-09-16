from datetime import datetime
import time

from django.core.cache import cache


class TestAddingLinks:
    """Testing adding functional with valid and invalid data"""

    def test_01_valid_adding_sites(self, client, valid_data, clear_cache):
        response = client.post('http://127.0.0.1:8000/visited_links/',
                               data=valid_data, content_type='application/json')
        assert response.status_code == 201
        assert response.data['status'] == 'ok'

    def test_02_adding_sites_wit_invalid_data(self, client, invalid_data):
        data_invalid_key, data_invalid_site = invalid_data
        response = client.post('http://127.0.0.1:8000/visited_links/',
                               data=data_invalid_key,
                               content_type='application/json')
        assert response.status_code == 400
        assert 'links' in response.data['status']
        assert response.data['status']['links'][0] == 'This field is required.'

        response = client.post('http://127.0.0.1:8000/visited_links/',
                               data=data_invalid_site,
                               content_type='application/json')
        assert response.status_code == 400
        link = data_invalid_site['links'][0]
        assert response.data['status'] == f"Object < {link} > is not a link"


class TestListDomains:
    """
    Testing default request (without parameters) and with different
    variations of "from" and "to"
    """

    def test_03_list_visits(self, client, valid_data, clear_cache):
        response = client.post('http://127.0.0.1:8000/visited_links/',
                               data=valid_data, content_type='application/json')
        assert response.status_code == 201
        response = client.get('http://127.0.0.1:8000/visited_domains/')
        assert len(response.data['domains']) == len(valid_data['links'])
        assert response.data['status'] == 'ok'

    def test_04_list_filter_visits(self, client, link_list, clear_cache):
        start_time = int(time.time())

        for i in link_list[:3]:
            cache.set(i, datetime.now())

        time.sleep(2)
        medium_time = int(time.time())

        for i in link_list[3:]:
            cache.set(i, datetime.now())

        time.sleep(2)
        end_time = int(time.time())

        # From parameter test
        response = client.get(
            f'http://127.0.0.1:8000/visited_domains/?from={start_time}')
        assert response.status_code == 200
        assert len(response.data['domains']) == 4
        response = client.get(
            f'http://127.0.0.1:8000/visited_domains/?from={medium_time}')
        assert len(response.data['domains']) == 1
        response = client.get(
            f'http://127.0.0.1:8000/visited_domains/?from={end_time}')
        assert len(response.data['domains']) == 0

        # To parameter test
        response = client.get(
            f'http://127.0.0.1:8000/visited_domains/?to={start_time}')
        assert response.status_code == 200
        assert len(response.data['domains']) == 0
        response = client.get(
            f'http://127.0.0.1:8000/visited_domains/?to={medium_time}')
        assert len(response.data['domains']) == 3
        response = client.get(
            f'http://127.0.0.1:8000/visited_domains/?to={end_time}')
        assert len(response.data['domains']) == 4

        # From and To parameters test
        response = client.get(
            'http://127.0.0.1:8000/visited_domains/'
            f'?from={start_time}&to={medium_time}')
        assert response.status_code == 200
        assert len(response.data['domains']) == 3
        response = client.get(
            'http://127.0.0.1:8000/visited_domains/'
            f'?from={medium_time}&to={end_time}')
        assert len(response.data['domains']) == 1
        response = client.get(
            'http://127.0.0.1:8000/visited_domains/'
            f'?from={start_time}&to={end_time}')
        assert len(response.data['domains']) == 4
