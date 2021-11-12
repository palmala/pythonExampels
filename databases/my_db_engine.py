import sqlite3

class my_db_engine:

    def __init__(self, **kwargs):
        self._filename = kwargs.get('filename')
        self._table = kwargs.get('table')

    @property
    def _filename(self):
        return self._dbfilename

    @_filename.setter
    def _filename(self, filename):
        self._dbfilename = filename
        self._db = sqlite3.connect(self._dbfilename)
        self._db.row_factory = sqlite3.Row

    @_filename.deleter
    def _filename(self):
        self.close()

    def close(self):
        self._db.close()
        del self._dbfilename
