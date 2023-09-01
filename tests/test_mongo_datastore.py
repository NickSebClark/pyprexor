from pyprexor_datastore.mongo import MongoDataStore
import mongomock
import pytest
import pymongo


@mongomock.patch(servers=(("server.example.com", 27017),))
def test_write_read_parameter_set():
    """Write a parameter set and read it back"""
    store = MongoDataStore("server.example.com")

    parameter_set = {"param": 1, "param2": "two"}

    inserted_id = store.write_parameter_set(parameter_set)

    read_parameter_set = store.get_parameter_set(inserted_id)

    assert parameter_set == read_parameter_set


@mongomock.patch(servers=(("server.example.com", 27017),))
def test_read_parameter_set_not_present():
    """Check we get a KeyError when parameter set is not available"""
    store = MongoDataStore("server.example.com")

    with pytest.raises(KeyError):
        store.get_parameter_set("1")


def test_bad_connection():
    """Check a bad URI fails on open"""
    with pytest.raises(pymongo.errors.ServerSelectionTimeoutError):
        MongoDataStore("Invalid URI")


@mongomock.patch(servers=(("server.example.com", 27017),))
def test_write_read_process_data():
    """Write and read back some process data"""
    store = MongoDataStore("server.example.com")

    process_data_1 = {"value1": "A", "value2": 2}
    process_data_2 = {"value1": "B", "value2": 3}

    store.write_process_data(process_data_1)
    store.write_process_data(process_data_2)

    returned_data = store.read_all_process_data()

    assert returned_data == [process_data_1, process_data_2]
