import os
import socket
from datetime import datetime
import pytz
from db import Database

async def get_status():
    db = Database()
    result = db.get_all(table="power_status")
    return result

async def update_status(metric: str,
                        value: str):
    db = Database()
    db.update_status(table="power_status",
                     metric=metric,
                     value=value)

async def get_interval(t1: str,
                       t2: str):
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
    now = datetime.now(pytz.timezone('Europe/Kyiv'))
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    status_data = await get_status()
    known_status = status_data["status"]
    last_power_off = status_data["last_power_off"]
    last_power_on = status_data["last_power_on"]
    power = await telnet()
    interval_previous = await get_interval(t1=last_power_off,
                                           t2=last_power_on)

    if known_status == power and power == "OK":
        interval = await get_interval(t1=timestamp,
                                      t2=last_power_on)
        await update_status(metric="interval", value=interval)
    if known_status == power and power == "ERR":
        interval = await get_interval(t1=timestamp,
                                      t2=last_power_off)
        await update_status(metric="interval", value=interval)
    elif known_status != power:
        interval = await get_interval(t1=timestamp,
                                      t2=last_power_off)
        await update_status(metric="interval", value=interval)

        await update_status(metric="status", value=power)

    if known_status == power:
        pass
    elif known_status == "OK" and power == "ERR":
        await update_status(metric="last_power_off", value=timestamp)
    elif known_status == "ERR" and power == "OK":
        await update_status(metric="last_power_on", value=timestamp)

    await update_status(metric="updated", value=timestamp)
    await update_status(metric="interval_previous", value=interval_previous)

async def telnet():
    """
    Check if a specific port on a host is open.
    Returns True if the port is open, False otherwise.
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
