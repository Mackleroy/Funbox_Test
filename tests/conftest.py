import pytest

from django.core.cache import cache


@pytest.fixture()
def clear_cache():
    yield
    cache.clear()


@pytest.fixture()
def link_list():
    return [
        "https://yandex.ru",
        "https://ya.ru?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270/"
    ]


@pytest.fixture()
def valid_data():
    data = {"links": [
        "https://yandex.ru",
        "https://ya.ru?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270/"
    ]}
    return data


@pytest.fixture()
def invalid_data():
    data_invalid_key = {"link": [
        'funxox.ru'
    ]}
    data_invalid_site = {"links": [
        "funboxru",
    ]}
    return data_invalid_key, data_invalid_site
