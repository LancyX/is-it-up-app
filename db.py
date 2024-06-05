"""Iteraction with sqlite database"""
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
        getting all rows from table
        """
        connection = self.connect()
        cur = connection.cursor()
        cur.execute(f'''SELECT status, updated, interval
                    FROM {table} WHERE inserted > datetime("now", "-7 days") ORDER BY id DESC''')
        rows = cur.fetchall()
        result = [{k: row[k] for k in row.keys()} for row in rows]
        return result

    def get_last(self, table: str):
        """
        getting last row from table
        """
        connection = self.connect()
        cur = connection.cursor()
        cur.execute(f'''SELECT * FROM {table} WHERE inserted > datetime("now", "-7 days")
                    AND id = (SELECT MAX(id) FROM {table})''')
        rows = cur.fetchall()
        result = [{k: row[k] for k in row.keys()} for row in rows]
        return result[0]

    def get_prev(self, table: str):
        """
        getting all rows from table
        """
        connection = self.connect()
        cur = connection.cursor()
        cur.execute(f'''SELECT * FROM {table} WHERE inserted > datetime("now", "-7 days")
                    AND id = (SELECT MAX(id) FROM {table}) - 1''')
        rows = cur.fetchall()
        result = [{k: row[k] for k in row.keys()} for row in rows]
        return result[0]

    def update_status(self, table: str,
                      metric: str, value: str):
        """
        update status in rows
        """
        connection = self.connect()
        cur = connection.cursor()

        # Update the row with the new values, except for the id
        cur.execute(f'''UPDATE {table} SET {metric} = "{value}"
                    WHERE id = (SELECT MAX(id) FROM {table})''')
        connection.commit()

    def insert_status_row(self, table: str,
                          data: dict):
        """
        update status in rows
        """
        connection = self.connect()
        cur = connection.cursor()

        # Update the row with the new values, except for the id
        # cur.execute(f'''INSERT INTO {table}
        #             (status, updated, last_power_on, last_power_off, interval, interval_previous, inserted)
        #             VALUES ("{data["status"]}", "{data["updated"]}", "{data["last_power_on"]}",
        #             "{data["last_power_off"]}", "{data["interval"]}",
        #             "{data["interval_previous"]}", "{data["inserted"]}" )''')
        cur.execute(f'''INSERT INTO {table}
                    (status, updated, interval, interval_previous, inserted)
                    VALUES ("{data["status"]}", "{data["updated"]}", "{data["interval"]}",
                    "{data["interval_previous"]}", "{data["inserted"]}" )''')
        connection.commit()
