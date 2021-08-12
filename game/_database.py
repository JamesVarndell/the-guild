
import json


class DatabaseManager:

    TABLE = None
    PRIMARY_KEY = 'id'

    def __init__(self, db, id):

        self.db = db
        self.id = id
    
    @property
    def table(self):
        if self.TABLE is None:
            raise NotImplementedError("No table configured for manager")
        return self.TABLE

    @property    
    def data(self):
        data = self.db.execute(
            f"SELECT * FROM {self.table} WHERE {self.PRIMARY_KEY} = ?",
            (self.id,)
        ).fetchone()
        return data

    def __getattr__(self, key):
        try:
            value = self.data[key]
        except (IndexError, KeyError):
            raise AttributeError(f"{self.table} has no column {key}")
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
        if isinstance(value, dict):
            value = DataManager(value, db_manager=self, db_key=key)
        return value

    def update(self, key, value):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.db.execute(
            f"UPDATE {self.table} "
            f"SET {key} = ? "
            f"WHERE {self.PRIMARY_KEY} = {self.id}",
            (value,)
        )
        self.db.commit()


class DataManager(dict):

    def __init__(self, *args, db_manager=None, db_key=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._db_manager = db_manager
        self._db_key = db_key

    def __setitem__(self, item, value):
        super().__setitem__(item, value)
        if self._db_manager is not None:
            self._db_manager.update(self._db_key, self)

    def __getattr__(self, key):
        try:
            value = self[key]
        except KeyError:
            raise AttributeError(f"{self._db_key} has no attribute {key}")
        return value
