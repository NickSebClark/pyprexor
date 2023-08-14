import pyprexor.datastore as datastore
import pytest


@pytest.fixture
def default_data():
    return [{"id": 2, "param": 8}, {"id": 3, "param": 9}, {"id": 4, "param": 10}]


def test_init_re_index(default_data):
    store = datastore.InMemoryDataStore(default_data, re_index=True)

    default_data[0]["id"] = 0

    assert default_data[0] == store.get_parameter_set(0)


def test_init(default_data):
    store = datastore.InMemoryDataStore(default_data)

    assert default_data[0] == store.get_parameter_set(2)
