from config import mongo_client


def remove_fields_from_test_data(dict_):
    del dict_['_id']

    return dict_


def set_test_database_data(collection, obj):
    mongo_client.client.db.get_collection(collection).insert(obj)
    mongo_client.client.close()


def clear_test_database(collection):
    mongo_client.client.db.get_collection(collection).drop()
    mongo_client.client.close()
