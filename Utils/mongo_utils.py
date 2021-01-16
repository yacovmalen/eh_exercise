"""
Mongo Connection Class - creates and maintains a connector mongo and utils to access and update the database
"""
import datetime
import os

from bson.json_util import dumps, loads
from pymongo import MongoClient
from Resources.errors import EntityAlreadyExistsError, DatabaseError, EntityNotFound

mongodb_ip = os.environ.get('MONGODB_IP', 'localhost')


class MongoConnector(object):
    def __init__(self):
        self.client = MongoClient(mongodb_ip, 27020)
        self.connectors = {
            'sessions':
            SessionConnector(self.client, 'sessions'),
            'meetings_resource':
            MeetingsResourceConnector(self.client, 'meetings_resource')
        }


class EntityConnector(object):
    def __init__(self, mongo_connection, collection):
        self.conn = mongo_connection
        self.collection = self.conn.db.get_collection(collection)

    def create_entity(self, entity):
        if 'entity_id' not in entity or not entity['entity_id']:
            entity['entity_id'] = self.get_last_id() + 1
        elif self._is_exist(entity['entity_id']):
            raise EntityAlreadyExistsError('Entity already exists', None)

        response = self._insert_or_update(entity, upsert=True)

        if '_id' in response:
            del response['_id']

        return response

    def get_one_or_all_entities(self, entity=None, return_empty=True):
        entity = entity or {}
        entity.update({'deleted': {'$exists': False}})
        docs = self.collection.find(entity)

        if not return_empty and (not docs or docs.count()) == 0:
            raise EntityNotFound('No entity {} found'.format(entity), None)
        return list(docs)

    def delete_entity(self, entity, hard_delete=False):
        entity.update({'deleted': datetime.datetime.utcnow()})
        return self.update_entity(entity)

    def update_entity(self, entity):
        response = self._insert_or_update(entity, upsert=False)

        if response == 'null' or not response:
            raise EntityNotFound('No entity {} found'.format(entity), None)

        return [res for res in response]

    def _insert_or_update(self, entity, upsert=False):
        now = datetime.datetime.utcnow()
        entity.update({'last_update': now})

        return self.collection.find_and_modify(
            {
                'entity_id': entity['entity_id'],
                'deleted': {
                    '$exists': False
                }
            }, {
                '$set': entity,
                '$setOnInsert': {
                    'creation_date': now
                }
            },
            upsert=upsert,
            new=True)

    def _hard_delete(self, query):
        try:
            return self.collection.remove(query)
        except Exception as e:
            print(e)
            raise DatabaseError('Database error', e)

    def _is_exist(self, entity_id):
        try:
            return self.collection.find_one({
                'entity_id': entity_id,
                'deleted': {
                    '$exists': False
                }
            })
        except Exception as e:
            print(e)
            raise DatabaseError('Database error', e)


class SessionConnector(EntityConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_participants(self, meeting_id, num_participants):
        if self._is_exist(str(meeting_id)):
            return self.update_entity({
                'entity_id': str(meeting_id),
                'num_participants': num_participants,
                'updated': datetime.datetime.utcnow()
            })
        else:
            return self.create_entity({
                'entity_id': str(meeting_id),
                'num_participants': num_participants,
            })

    def end_session(self, meeting_id, num_participants=0):
        if self._is_exist(str(meeting_id)):
            return self.delete_entity({
                'entity_id': str(meeting_id),
                'num_participants': num_participants,
            })
        else:
            return []


class MeetingsResourceConnector(EntityConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def lock_meeting(self, meeting_id=None, url=None):
        query = {'entity_id': str(meeting_id)} if meeting_id else {'locked': False}
        slot = self.get_one_or_all_entities(query)
        slot = slot[0] if slot else []
        
        if not slot:
            return self.create_entity({
                'entity_id': str(meeting_id),
                'url': url,
                'locked': True,
                'lock_time': datetime.datetime.utcnow()
            })

        if slot and not slot.get('locked'):
            return self.update_entity({
                'entity_id': str(slot.get('entity_id', '')),
                'locked': True,
                'lock_time': datetime.datetime.utcnow()
            })
        return slot

    def release_meeting(self, meeting_id=None):
        if self._is_exist(str(meeting_id)):
            return self.update_entity({
                'entity_id': str(meeting_id),
                'locked': False,
                'lock_time': None
            })
