"""Basic functions for appd"""
import os
import socket
import locale
from datetime import datetime
import pytz
from db import Database
from translation import read_translation

FORMAT_STR = "%Y-%m-%d %H:%M"
LANGUAGE = os.getenv('LANGUAGE')

def get_mode():
    """return mode value"""
    data = os.getenv('MODE')
    return data

async def get_all_status():
    """return all data from table"""
    db = Database()
    result = await db.get_all(table="power_status")
    return result

async def get_last_status():
    """return most recent data from table"""
    db = Database()
    result = await db.get_last(table="power_status")
    return result

async def get_prev_status():
    """return previous status data from table"""
    db = Database()
    result = await db.get_prev(table="power_status")
    return result

async def update_status(metric: str,
                        value: str):
    """update values in rows"""
    db = Database()
    await db.update_status(table="power_status",
                           metric=metric,
                           value=value)

async def insert_new_status(data: dict):
    """insert new row"""
    db = Database()
    await db.insert_status_row(table="power_status",
                               data=data)

async def get_interval(t1: str,
                       t2: str):
    """return diff between 2 given timestamps"""
    dt1 = datetime.strptime(t1, FORMAT_STR)
    dt2 = datetime.strptime(t2, FORMAT_STR)

    if dt1 > dt2:
        time_diff = dt1 - dt2
    else:
        time_diff = dt2 - dt1

    years = abs(time_diff.days // 365)
    months = abs((time_diff.days % 365) // 30)
    days = abs(time_diff.days % 365 % 30)
    hours = abs(time_diff.seconds // 3600)
    minutes = abs((time_diff.seconds % 3600) // 60)

    data = await read_translation(language=LANGUAGE)
    diff_text = data["time_diff"]

    # Format the difference
    formatted_diff = ""
    if years:
        formatted_diff += f"{years} {diff_text['years']}, "
    if months:
        formatted_diff += f"{months} {diff_text['months']}, "
    if days:
        formatted_diff += f"{days} {diff_text['days']}, "
    if hours:
        formatted_diff += f"{hours} {diff_text['hours']}, "
    if minutes:
        formatted_diff += f"{minutes} {diff_text['minutes']}, "

    interval = formatted_diff.strip(", ")
    return interval

async def get_time():
    """return timestamp for updating rows"""
    data = await read_translation(language=LANGUAGE)
    data = data["time"]
    locale.setlocale(locale.LC_TIME, data["locale"])
    if data["timezone"] == "UTC":
        now = datetime.now(pytz.utc)
    else:
        now = datetime.now(pytz.timezone(data["timezone"]))
    return now

async def get_day_of_week(now: object):
    """return day of week, starting with capital letter"""
    day_name = now.strftime("%A")
    day_name_tittle = day_name.title()
    return day_name_tittle

async def crontask():
    """main task which checks telnet connection and updates statuses"""
    now = await get_time()
    timestamp = now.strftime(FORMAT_STR)

    day_of_week = await get_day_of_week(now=now)

    status_data = await get_last_status()
    known_status = status_data["status"]

    power = await telnet()
    prev = await get_prev_status()
    interval_previous = await get_interval(t1=prev["inserted"],
                                           t2=status_data["inserted"])

    if known_status == power:
        interval = await get_interval(t1=timestamp,
                                      t2=status_data["inserted"])

    elif known_status != power:
        translation = await read_translation(language=LANGUAGE)
        interval = translation['time_diff']['minutes']
        interval = "0 " + interval

    if known_status == power:
        await update_status(metric="updated", value=timestamp)
        await update_status(metric="interval", value=interval)
        await update_status(metric="interval_previous", value=interval_previous)
        await update_status(metric="day_of_week", value=day_of_week)

    else:
        data = {
                "status": power,
                "updated": timestamp,
                "interval": interval,
                "interval_previous": interval_previous,
                "inserted": timestamp,
                "day_of_week": day_of_week
                }

        await insert_new_status(data=data)

async def telnet():
    """
    Check if a specific port on a host is open.
    Returns OK if the port is open, ERR otherwise.
    """
    host = os.getenv("CHECK_HOST")
    port = int(os.getenv("CHECK_PORT"))
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
    with open(f"../frontend/html/{source}.html", "r", encoding="utf-8") as file:
        # Reading from a file
        return file.read()
