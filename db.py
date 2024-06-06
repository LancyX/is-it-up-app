"""Iteraction with sqlite database"""
import sqlite3

class Database():
    """
    db interaction
    """

    async def connect(self):
        """
        connect to db
        """
        connection = sqlite3.connect('home_monitor.db')
        connection.row_factory = sqlite3.Row
        return connection

    async def get_all(self, table: str):
        """
        getting all rows from table
        """
        connection = await self.connect()
        cur = connection.cursor()
        cur.execute(f'''SELECT status, inserted, interval, day_of_week
                    FROM {table} WHERE inserted > datetime("now", "-7 days") ORDER BY id DESC''')
        rows = cur.fetchall()
        result = [{k: row[k] for k in row.keys()} for row in rows]
        return result

    async def get_last(self, table: str):
        """
        getting last row from table
        """
        connection = await self.connect()
        cur = connection.cursor()
        cur.execute(f'''SELECT * FROM {table} WHERE inserted > datetime("now", "-7 days")
                    AND id = (SELECT MAX(id) FROM {table})''')
        rows = cur.fetchall()
        result = [{k: row[k] for k in row.keys()} for row in rows]
        return result[0]

    async def get_prev(self, table: str):
        """
        getting all rows from table
        """
        connection = await self.connect()
        cur = connection.cursor()
        cur.execute(f'''SELECT * FROM {table} WHERE inserted > datetime("now", "-7 days")
                    AND id = (SELECT MAX(id) FROM {table}) - 1''')
        rows = cur.fetchall()
        result = [{k: row[k] for k in row.keys()} for row in rows]
        return result[0]

    async def update_status(self, table: str,
                      metric: str, value: str):
        """
        update status in rows
        """
        connection = await self.connect()
        cur = connection.cursor()

        # Update the row with the new values, except for the id
        cur.execute(f'''UPDATE {table} SET {metric} = "{value}"
                    WHERE id = (SELECT MAX(id) FROM {table})''')
        connection.commit()

    async def insert_status_row(self, table: str,
                          data: dict):
        """
        update status in rows
        """
        connection = await self.connect()
        cur = connection.cursor()

        cur.execute(f'''INSERT INTO {table}
                    (status, updated, interval, interval_previous, inserted, day_of_week)
                    VALUES ("{data["status"]}", "{data["updated"]}", "{data["interval"]}",
                    "{data["interval_previous"]}", "{data["inserted"]}",
                    "{data["day_of_week"]}" )''')
        connection.commit()
