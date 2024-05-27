from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from basic import read_file, crontask

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

scheduler.add_job(crontask, 'interval', minutes=1)

@app.get("/api/data")
async def get_data():
    last_change = read_file("last-change")
    power = read_file("status")
    updated = read_file("updated")

    data = {"power": power,
            "timestamp": updated,
            "last_change": last_change}

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
                if (data.power == 1) {
                    power_text = 'наявне'
                } else {
                    power_text = 'відсутнє'
                }
                document.getElementById('power').innerHTML = '<strong>Електропостачання</strong>: ' + power_text;
                document.getElementById('timestamp').innerHTML = '<strong>Час оновлення данних</strong>: ' + data.timestamp;
                document.getElementById('last_change').innerHTML = '<strong>Остання зміна статусу</strong>: ' + data.last_change;
                const img = document.getElementById('power_img');
                img.src = data.power == 1 ? '/static/img/power-on.png' : '/static/img/power-off.png';
            }

            setInterval(fetchData, 30000);  // Fetch data every 30 seconds
            window.onload = fetchData;
        </script>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
            }

            .container {
                text-align: center;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
            }

            h1 {
                font-size: 2em;
                margin-bottom: 20px;
            }

            p {
                font-size: 1em;
                margin: 10px 0;
            }

            img {
                width: 150px;
                height: 150px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>вул. Машинобудівників, буд. 23</h1>
            <img id="power_img" src="/static/img/power-off.png" alt="Power Status">
            <p id="power"><strong>Електропостачання</strong>: </p>
            <p id="timestamp"><strong>Час оновлення данних</strong>: </p>
            <p id="last_change"><strong>Остання зміна статусу</strong>: </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
