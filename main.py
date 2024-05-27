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

@app.get("/", response_class=HTMLResponse)
async def read_root():

    last_change = read_file("last-change")
    power = read_file("status")
    updated = read_file("updated")


    # Determine the image to display based on the power value
    if power == "1":
        image_url = "/static/img/power-on.png"
        power = "наявне"
    else:
        image_url = "/static/img/power-off.png"
        power = "відсутнє"

    # Render the HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ua">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Power Status</title>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
    </head>
    <body>
        <div class="container">
            <h1>вул. Машинобудівників, буд. 23</h1>
            <img src="{image_url}" alt="Power Status" width="150" height="150">
            <p><b>Електропостачання</b>: {power}</p>
            <p><b>Час оновлення данних</b>: {updated}</p>
            <p><b>Остання зміна статусу</b>: {last_change}</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
