import pyprexor_datastore.datastore as datastore
import pytest


@pytest.fixture
def default_data():
    return [{"id": 2, "param": 8}, {"id": 3, "param": 9}, {"id": 4, "param": 10}]


def test_init_re_index(default_data):
    """Test a new InMemoryDatastore with the re_index option. Check the id of the first element is set to 0."""
    store = datastore.InMemoryDataStore(default_data, re_index=True)

    default_data[0]["id"] = "0"

    assert default_data[0] == store.get_parameter_set("0")


def test_init(default_data):
    """Test a new InMemoryDatastore with default parameters"""
    store = datastore.InMemoryDataStore(default_data)

    assert default_data[0] == store.get_parameter_set(2)


def test_read_write_process_data(default_data):
    """Round trip of process data."""

    store = datastore.InMemoryDataStore({})

    store.write_process_data(default_data[0])
    store.write_process_data(default_data[1])

    returned_process_data = store.read_all_process_data()

    assert returned_process_data == [default_data[0], default_data[1]]
