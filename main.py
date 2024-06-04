from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from basic import crontask, get_status

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the scheduler
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Set up rate limiting

    # Start the scheduler
    scheduler.start()

    # Yield control to the application
    yield

    # Clean up resources on shutdown
    scheduler.shutdown()

app.router.lifespan_context = lifespan

scheduler.add_job(crontask, 'interval', seconds=30)

@app.get("/api/data")
async def get_data():
    status_data = await get_status()
    power = status_data["status"]
    updated = status_data["updated"]
    last_power_on = status_data["last_power_on"]
    last_power_off = status_data["last_power_off"]
    interval_previous = status_data["interval_previous"]
    interval = status_data["interval"]

    data = {
            "power": power,
            "timestamp": updated,
            "last_power_on": last_power_on,
            "last_power_off": last_power_off,
            "interval_previous": interval_previous,
            "interval": interval
            }

    return data

@app.get("/", response_class=HTMLResponse)
async def read_root():

    # Render the HTML template
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Power Status</title>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
        <script>
            async function fetchData() {
                const response = await fetch('/api/data');
                const data = await response.json();
                let power_text;
                if (data.power == "OK") {
                    power_text = 'Наявне впродовж'
                } else {
                    power_text = 'Відсутнє впродовж'
                }

                let last_power_text;
                if (data.power == "OK") {
                    last_power_text = 'Було відсутнє впродовж'
                } else {
                    last_power_text = 'Було наявне впродовж'
                }

                document.getElementById('power').innerHTML = '<strong>' + power_text + '</strong>: ' + data.interval;
                document.getElementById('timestamp').innerHTML = '<strong>Дані оновлено</strong>: ' + data.timestamp;
                document.getElementById('interval').innerHTML = '<strong>' + last_power_text + '</strong>: ' + data.interval_previous;
                document.getElementById('last_power_on').innerHTML = '<strong>Останнє включення</strong>: ' + data.last_power_on;
                document.getElementById('last_power_off').innerHTML = '<strong>Останнє відключення</strong>: ' + data.last_power_off;
                const img = document.getElementById('power_img');
                img.src = data.power == "OK" ? '/static/img/power-on.png' : '/static/img/power-off.png';
            }

            setInterval(fetchData, 30000);  // Fetch data every 30 seconds
            window.onload = fetchData;
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Вишневе</h1>
            <h1>вул. Машинобудівників, буд. 23</h1>
            <img id="power_img" src="/static/img/power-off.png" alt="Power Status">
            <h3><strong>Поточні дані</strong>:</h3>
            <p id="power"><strong>Електропостачання</strong>: </p>
            <p id="timestamp"><strong>Дані оновлено</strong>: </p>
            <h3><strong>Попередні дані</strong>:</h3>
            <p id="interval"><strong>|</strong></p>
            <p id="last_power_on"><strong>Останнє включення</strong>: </p>
            <p id="last_power_off"><strong>Останнє відключення</strong>: </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
