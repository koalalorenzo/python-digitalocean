# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE, PUT

__SIZE_SLUG__ = [
    'db-s-1vcpu-1gb',
    'db-s-1vcpu-2gb',
    'db-s-2vcpu-4gb',
    'db-s-4vcpu-8gb',
    'db-s-6vcpu-16gb',
    'db-s-8vcpu-32gb',
    'db-s-16vcpu-64gb'
]

__DB_ENGINES__ = {
    'pg': {
        'versions': ['10','11']
    },
    'mysql': {
        'versions': ['8']
    },
    'redis':{
        'versions': ['5']
    }
}


class DatabaseCreate(BaseAPI):

    def __init__(self, *args, **kwargs):
        super(DatabaseCreate, self).__init__(*args, **kwargs)


    def cluster(self, name, engine, size, region, num_nodes, version=None, tags=None):
        if __DB_ENGINES__[engine]:
            params = {
                "name": name,
                "engine": engine,
                "size": size,
                "region": region,
                "num_nodes": int(num_nodes)
            }
        if version:
            if version in __DB_ENGINES__[engine]['versions']:
                params['version'] = version
            else:
                raise AttributeError('Please provide a valid database version')
        if tags and isinstance(tags, list):
            params['tags'] = tags

        data = self.get_data('databases/', type=POST, params=params)

        if data:
            return data['database']
        else:
            return 'Error creating database'

    def replica(self, name, size, region=None, tags=None, db_id=None):
        params = {}
        params['name'] = name
        if size in __SIZE_SLUG__:
            params['size'] = size
        if region:
            params['region'] = region
        if tags:
            params['tags'] = tags

        if db_id:
            data = self.get_data("databases/{}/replicas".format(db_id), type='POST', params=params)
        else:
            data = self.get_data("databases/{}/replicas".format(self.id), type='POST', params=params)

        if data:
            return data['replica']
        else:
            return 'Error creating replica'

    def user(self, name, db_id=None):
        params = {}
        params['name'] = name

        if db_id:
            data = self.get_data("databases/{}/users".format(db_id), type='POST', params=params)
        else:
            data = self.get_data("databases/{}/users".format(self.id), type='POST', params=params)

        if data:
            return data['users']
        else:
            return 'Error creating users'

    def database(self, name, db_id=None):
        params = {}
        params['name'] = name

        if db_id:
            data = self.get_data("databases/{}/dbs".format(db_id), type='POST', params=params)
        else:
            data = self.get_data("databases/{}/dbs".format(self.id), type='POST', params=params)

        if data:
            return data['db']
        else:
            return 'Error creating database'


class DatabaseList(BaseAPI):

    def __init__(self, *args, **kwargs):
        super(DatabaseList, self).__init__(*args, **kwargs)

    def clusters(self, tag_name=None):
        if tag_name:
            data = self.get_data("databases?tag_name={}".format(tag_name))
        else:
            data = self.get_data("databases")
        return None if not data else data['databases']

    def backups(self, db_id):
        data = self.get_data("databases/{}/backups".format(db_id))
        return None if not data else data['backups']

    def replicas(self, db_id):
        data = self.get_data("databases/{}/replicas".format(db_id))
        return None if not data else data['replicas']
       
    def users(self, db_id):
        data = self.get_data("databases/{}/users".format(db_id))
        return None if not data else data['users']

    def databases(self, db_id):
        data = self.get_data("databases/{}/dbs".format(db_id))
        return None if not data else data['dbs']


class DatabaseGet(BaseAPI):

    def __init__(self, *args, **kwargs):
        super(DatabaseGet, self).__init__(*args, **kwargs)

    def cluster(self, db_id):
        data = self.get_data("databases/{}".format(db_id))
        return None if not data else data['database']

    def replica(self, db_id, replica_name):
        data = self.get_data("databases/{}/replicas/{}".format(db_id, replica_name))
        return None if not data else data['replica']
    
    def user(self, db_id, username):
        data = self.get_data("databases/{}/users/{}".format(db_id, username))
        return None if not data else data['user']


class DatabaseDestroy(BaseAPI):

    def __init__(self, *args, **kwargs):
        super(DatabaseDestroy, self).__init__(*args, **kwargs)

    def cluster(self, db_id):
        data = self.get_data("databases/{}".format(db_id), type='DELETE')
        return None if not data else True

    def replica(self, db_id, replica_name):
        data = self.get_data("databases/{}/replicas/{}".format(db_id, replica_name), type='DELETE')
        return None if not data else True

    def user(self, db_id, username):
        data = self.get_data("databases/{}/users/{}".format(db_id, username), type='DELETE')
        return None if not data else True

    def database(self, db_id, db_name):
        data = self.get_data("databases/{}/dbs/{}".format(db_id, db_name), type='DELETE')
        return None if not data else True

class Database(BaseAPI):

    def __init__(self, *args, **kwargs):
        super(Database, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs
        pass

    @property
    def create(self):
        return DatabaseCreate(*self.args, **self.kwargs)

    @property
    def destroy(self):
        return DatabaseDestroy(*self.args, **self.kwargs)

    @property
    def list(self):
        return DatabaseList(*self.args, **self.kwargs)

    @property
    def get(self):
        return DatabaseGet(*self.args, **self.kwargs)

    def resize(self, size, num_nodes, db_id):
        params = {}
        if size in __SIZE_SLUG__:
            params['size'] = size
        params['num_nodes'] = int(num_nodes)
        data = self.get_data('databases/{}/resize'.format(db_id), type='PUT', params=params)
        return None if not data else True

    def migrate(self, region, db_id):
        params = {}
        params['region'] = region
        data = self.get_data('databases/{}/migrate'.format(db_id), type='PUT', params=params)
        return None if not data else True

    def maintenance(self, day, hour, db_id):
        params = {}
        params['day'] = day
        params['hour'] = hour
        data = self.get_data('databases/{}/maintenance'.format(db_id), type='PUT', params=params)
        return None if not data else True
    
