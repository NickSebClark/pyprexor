import pyprexor_datastore.datastore as datastore
import pytest


def test_abstract_datastore():
    store = datastore.Datastore()

    with pytest.raises(NotImplementedError):
        store.get_parameter_set(1)

    with pytest.raises(NotImplementedError):
        store.write_process_data({})
