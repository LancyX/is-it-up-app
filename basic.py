"""Basic functions for appd"""
import os
import socket
from datetime import datetime
import pytz
from db import Database

async def get_all_status():
    """return all data from table"""
    db = Database()
    result = db.get_all(table="power_status")
    return result

async def get_last_status():
    """return most recent data from table"""
    db = Database()
    result = db.get_last(table="power_status")
    return result

async def get_prev_status():
    """return previous status data from table"""
    db = Database()
    result = db.get_prev(table="power_status")
    return result

async def update_status(metric: str,
                        value: str):
    """update values in rows"""
    db = Database()
    db.update_status(table="power_status",
                     metric=metric,
                     value=value)

async def insert_new_status(data: dict):
    """insert new row"""
    db = Database()
    db.insert_status_row(table="power_status",
                         data=data)

async def get_interval(t1: str,
                       t2: str):
    """return diff between 2 given timestamps"""
    format_str = "%Y-%m-%d %H:%M"
    dt1 = datetime.strptime(t1, format_str)
    dt2 = datetime.strptime(t2, format_str)

    if dt1 > dt2:
        time_diff = dt1 - dt2
    else:
        time_diff = dt2 - dt1

    years = abs(time_diff.days // 365)
    months = abs((time_diff.days % 365) // 30)
    days = abs(time_diff.days % 365 % 30)
    hours = abs(time_diff.seconds // 3600)
    minutes = abs((time_diff.seconds % 3600) // 60)

    # Format the difference
    formatted_diff = ""
    if years:
        formatted_diff += f"{years} років, "
    if months:
        formatted_diff += f"{months} місяців, "
    if days:
        formatted_diff += f"{days} днів, "
    if hours:
        formatted_diff += f"{hours} годин, "
    if minutes:
        formatted_diff += f"{minutes} хвилин, "

    interval = formatted_diff.strip(", ")
    return interval

async def crontask():
    """main task which checks telnet connection and updates statuses"""
    now = datetime.now(pytz.timezone('Europe/Kyiv'))
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    status_data = await get_last_status()
    known_status = status_data["status"]

    power = await telnet()
    prev = await get_prev_status()
    interval_previous = await get_interval(t1=prev["inserted"],
                                           t2=status_data["inserted"])

    if known_status == power:
        interval = await get_interval(t1=timestamp,
                                      t2=status_data["inserted"])

    elif known_status != power and power == "OK":
        interval = "0 хвилин"
    elif known_status != power and power == "ERR":
        interval = "0 хвилин"

    if known_status == power:
        await update_status(metric="updated", value=timestamp)
        await update_status(metric="interval", value=interval)
        await update_status(metric="interval_previous", value=interval_previous)
    else:
        data = {
                "status": power,
                "updated": timestamp,
                "interval": interval,
                "interval_previous": interval_previous,
                "inserted": timestamp
                }

        await insert_new_status(data=data)

async def telnet():
    """
    Check if a specific port on a host is open.
    Returns OK if the port is open, ERR otherwise.
    """
    host = os.getenv("HOME_HOST")
    port = int(os.getenv("HOME_PORT"))
    timeout = 5

    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        # Try to connect to the host and port
        sock.connect((host, port))
        return "OK"
    except socket.error:
        return "ERR"
    finally:
        sock.close()

async def read_html(source: str):
    """return desired html page content"""
    with open(f"html/{source}.html", "r", encoding="utf-8") as file:
        # Reading from a file
        return file.read()
