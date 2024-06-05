from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from basic import crontask, get_all_status, get_last_status, get_prev_status, read_html

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the scheduler
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Set up rate limiting"""

    # Start the scheduler
    scheduler.start()

    # Yield control to the application
    yield

    # Clean up resources on shutdown
    scheduler.shutdown()

app.router.lifespan_context = lifespan

scheduler.add_job(crontask, 'interval', seconds=30)

@app.get("/api/main")
async def get_data():
    """return json with data for frontend"""
    status = await get_last_status()
    prev_status = await get_prev_status()
    power = status["status"]
    updated = status["updated"]
    interval_previous = status["interval_previous"]
    interval = status["interval"]

    if status["status"] == "OK":
        last_power_on = status["inserted"]
        last_power_off = prev_status["inserted"]
    else:
        last_power_on = prev_status["inserted"]
        last_power_off = status["inserted"]

    data = {
            "power": power,
            "timestamp": updated,
            "last_power_on": last_power_on,
            "last_power_off": last_power_off,
            "interval_previous": interval_previous,
            "interval": interval
            }

    return data

@app.get("/api/prev-data")
async def get_prev_data_table():
    """return json with data for frontend"""
    data = await get_all_status()
    for item in data:
        if item["status"] == "OK":
            item["status"] = "Включення"
        elif item["status"] == "ERR":
            item["status"] = "Відключення"
    return data

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """return main.html with root page"""
    html_content = await read_html(source="main")
    # html_content = await read_html(source="maintenance")
    return HTMLResponse(content=html_content)

@app.get("/prev-data", response_class=HTMLResponse)
async def read_prev_data():
    """return main.html with root page"""
    html_content = await read_html(source="prev-data")
    return HTMLResponse(content=html_content)

@app.get("/contact", response_class=HTMLResponse)
async def read_contact():
    """return main.html with root page"""
    html_content = await read_html(source="contact")
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
