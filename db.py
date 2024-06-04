import sqlite3

class Database():
    """
    db interaction
    """

    def connect(self):
        """
        connect to db
        """
        connection = sqlite3.connect('home_monitor.db')
        connection.row_factory = sqlite3.Row
        return connection

    def get_all(self, table: str):
        """
        getting all tables for archivation
        with own parameters
        """
        connection = self.connect()
        cur = connection.cursor()
        cur.execute(f'SELECT * FROM {table}')
        rows = cur.fetchall()
        result = [{k: row[k] for k in row.keys()} for row in rows]
        return result[0]

    def update_status(self, table: str,
                      metric: str, value: str):
        """
        update status and last_row
        """
        connection = self.connect()
        cur = connection.cursor()

        # Update the row with the new values, except for the id
        cur.execute(f'UPDATE {table} SET {metric} = "{value}" WHERE id = 1')
        connection.commit()
