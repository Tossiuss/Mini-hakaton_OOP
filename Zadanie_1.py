#Это Задание

import json
import unittest



class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.db_name, 'r') as file:
                return json.load(file)
        except (FileNotFoundError):
            return []

    def _save_data(self):
        with open(self.db_name, 'w') as file:
            json.dump(self.data, file)

###

    def create(self, record):
        self.data.append(record)
        self._save_data()

###

    def read(self, record_id=None):
        if record_id is None:
            return self.data
        for record in self.data:
            if record.get('id') == record_id:
                return record

###

    def update(self, record_id, updated_data):
        for record in self.data:
            if record.get('id') == record_id:
                record.update(updated_data)
                self._save_data()
                return True
        return False

###

    def delete(self, record_id):
        for index, record in enumerate(self.data):
            if record.get('id') == record_id:
                del self.data[index]
                self._save_data()
                return True
        return False

###

    def close(self):
        self.data = []

###########################################################################################################################

class Model:
    def __init__(self, id, name, email, article):
        self.id = id
        self.name = name
        self.email = email
        self.article = article

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'article': self.article
        }

###########################################################################################################################

class View:
    @staticmethod
    def print_records(records):
        if not records:
            print("No records found.")
        else:
            for record in records:
                print(
                    f"ID: {record['id']}, Name: {record['name']}, Email: {record['email']}, Article: {record['article']}"
                )

    @staticmethod
    def print_message(message):
        print(message)

###########################################################################################################################

class Controller:
    def __init__(self, database):
        self.database = database

    def create_record(self, model_instance):
        self.database.create(model_instance.to_dict())

    def read_records(self):
        return self.database.read()

    def read_record(self, record_id):
        return self.database.read(record_id)

    def update_record(self, record_id, updated_data):
        return self.database.update(record_id, updated_data)

    def delete_record(self, record_id):
        return self.database.delete(record_id)

###########################################################################################################################

class TestCRUD(unittest.TestCase):
    def setUp(self):
        self.db = Database('test_db.json')
        self.controller = Controller(self.db)

    def tearDown(self):
        self.db.close()

    def test_create_record(self):
        record_data = {
            'id': 1,
            'name': 'John D',
            'email': 'john@example.com',
            'article': 'Fakts onli'
        }
        self.controller.create_record(Model(**record_data))
        self.assertEqual(len(self.db.read()), 1)

###

    def test_read_record(self):
        record_data = {
            'id': 1,
            'name': 'John D',
            'email': 'john@example.com',
            'article': 'Fakts onli'
        }
        self.controller.create_record(Model(**record_data))
        record = self.controller.read_record(1)
        self.assertEqual(record['name'], 'John D')

###

    def test_update_record(self):
        record_data = {
            'id': 1,
            'name': 'John D',
            'email': 'john@example.com',
            'article': 'Fakts onli'
        }
        self.controller.create_record(Model(**record_data))
        updated_data = {'name': 'John Smit', 'article': 'FAKTS'}
        self.controller.update_record(1, updated_data)
        record = self.controller.read_record(1)
        self.assertEqual(record['name'], 'John Smit')
        self.assertEqual(record['article'], 'FAKTS')
    
###

    # def test_delete_record(self):
    #     record_data = {
    #         'id': 1,
    #         'name': 'John D',
    #         'email': 'john@example.com',
    #         'article': 'Fakts onli'
    #     }
    #     self.controller.create_record(Model(**record_data))
    #     self.controller.delete_record(1)
    #     self.assertEqual(len(self.db.read()), 0)

if __name__ == '__main__':
    unittest.main()