from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from basic import crontask, get_all_status, get_last_status
from basic import get_prev_status, read_html, get_mode
from basic import read_translation, read_titles
from basic import LANGUAGE
from models import Translation

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Set up rate limiting"""
    # Start the scheduler
    print(app)
    scheduler.start()
    # Yield control to the application
    yield
    # Clean up resources on shutdown
    scheduler.shutdown()


app.router.lifespan_context = lifespan

MODE = get_mode()

if MODE != "MAINTENANCE":
    scheduler.add_job(crontask, "interval", seconds=30)

# API DATA Section


@app.get("/api/main")
async def get_data():
    """Return json with data for frontend"""
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

    return {
        "status": power,
        "timestamp": updated,
        "last_on": last_power_on,
        "last_off": last_power_off,
        "interval_previous": interval_previous,
        "interval": interval,
    }


@app.get("/api/table")
async def get_prev_data_table():
    """Return json with data for frontend"""
    return await get_all_status()


# API Translation Section


@app.post("/api/translation")
async def get_translation(request: Translation):
    """Return json with translation data for frontend"""
    data = await read_translation(language=LANGUAGE)
    return data[request.page]


@app.get("/api/titles")
async def get_titles():
    """Return json with titles data for frontend"""
    return await read_titles()


# HTML Section


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Return main.html with root page"""
    if MODE != "MAINTENANCE":
        html_content = await read_html(source="main")
    else:
        html_content = await read_html(source="maintenance")
    return HTMLResponse(content=html_content)


@app.get("/table", response_class=HTMLResponse)
async def read_table():
    """Return main.html with root page"""
    if MODE != "MAINTENANCE":
        html_content = await read_html(source="table")
    else:
        html_content = await read_html(source="maintenance")
    return HTMLResponse(content=html_content)


@app.get("/contact", response_class=HTMLResponse)
async def read_contact():
    """Return main.html with root page"""
    if MODE != "MAINTENANCE":
        html_content = await read_html(source="contact")
    else:
        html_content = await read_html(source="maintenance")
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)  # type: ignore[S104]
