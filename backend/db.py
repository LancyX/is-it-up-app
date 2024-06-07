"""Iteraction with sqlite database"""

import sqlite3


class Database:
    """DB interaction"""

    @staticmethod
    async def connect():
        """Connect to db"""
        connection = sqlite3.connect("monitor.db")
        connection.row_factory = sqlite3.Row
        return connection

    async def create_table_if_not_exist(self):
        """Create table if not present"""
        connection = await self.connect()
        cur = connection.cursor()
        cur.execute("""SELECT name FROM sqlite_master WHERE type='table'
                    AND name="power_status";""")
        exist = cur.fetchone()

        if not exist:
            table_schema = """
                            id INTEGER PRIMARY KEY,
                            status TEXT,
                            inserted TIMESTAMP,
                            day_of_week TEXT,
                            updated TIMESTAMP,
                            interval TEXT,
                            interval_previous TEXT
                            """
            cur.execute(f"CREATE TABLE IF NOT EXISTS power_status ({table_schema})")
            connection.commit()

            cur.execute("""INSERT INTO power_status (id,status,inserted,day_of_week,
                        updated, interval,interval_previous)
                        VALUES( "1","ERR","2024-06-06 16:25","Thursday",
                        "2024-06-06 19:24","1 hour","5 minutes");""")
            connection.commit()

            cur.execute("""INSERT INTO power_status (id,status,inserted,day_of_week,
                        updated, interval,interval_previous)
                        VALUES( "2","OK","2024-06-06 19:25","Thursday",
                        "2024-06-06 19:25","0 minutes","1 hour");""")
            connection.commit()

            cur.close()
            connection.close()

    async def get_all(self, table: str):
        """Get all rows from table"""
        await self.create_table_if_not_exist()

        connection = await self.connect()
        cur = connection.cursor()
        cur.execute(f"""SELECT status, inserted, interval, day_of_week
                    FROM {table} WHERE inserted > datetime("now", "-7 days")
                      ORDER BY id DESC""")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    async def get_last(self, table: str):
        """Get last row from table"""
        await self.create_table_if_not_exist()

        connection = await self.connect()
        cur = connection.cursor()
        cur.execute(f"""SELECT * FROM {table} WHERE inserted > datetime("now", "-7 days")
                    AND id = (SELECT MAX(id) FROM {table})""")
        rows = cur.fetchall()
        result = [dict(row) for row in rows]

        return result[0]

    async def get_prev(self, table: str):
        """Get all rows from table"""
        await self.create_table_if_not_exist()

        connection = await self.connect()
        cur = connection.cursor()
        cur.execute(f"""SELECT * FROM {table} WHERE inserted > datetime("now", "-7 days")
                    AND id = (SELECT MAX(id) FROM {table}) - 1""")
        rows = cur.fetchall()
        result = [dict(row) for row in rows]
        return result[0]

    async def update_status(self, table: str, metric: str, value: str):
        """Update status in rows"""
        await self.create_table_if_not_exist()

        connection = await self.connect()
        cur = connection.cursor()

        # Update the row with the new values, except for the id
        cur.execute(f"""UPDATE {table} SET {metric} = "{value}"
                    WHERE id = (SELECT MAX(id) FROM {table})""")
        connection.commit()

    async def insert_status_row(self, table: str, data: dict):
        """Update status in rows"""
        await self.create_table_if_not_exist()

        connection = await self.connect()
        cur = connection.cursor()

        cur.execute(f"""INSERT INTO {table}
                    (status, updated, interval, interval_previous, inserted, day_of_week)
                    VALUES ("{data["status"]}", "{data["updated"]}", "{data["interval"]}",
                    "{data["interval_previous"]}", "{data["inserted"]}",
                    "{data["day_of_week"]}" )""")
        connection.commit()
