import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from basic import ping, read_file, write_to_file, telnet

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():

    now = datetime.now()
    timestamp = now.strftime("%d/%m %H:%M:%S")

    last_change = read_file("last-change")
    known_status = read_file("status")

    if telnet(host=os.getenv("HOME_HOST"),
              port=int(os.getenv("HOME_PORT"))):
        power = "1"
    else:
        power = "0"

    if known_status == power:
        pass
    else:
        write_to_file(source="status", value=power)

    if known_status == power:
        pass
    else:
        write_to_file(source="last-change", value=timestamp)
        last_change = timestamp

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
            <p><b>Час оновлення данних</b>: {timestamp}</p>
            <p><b>Остання зміна статусу</b>: {last_change}</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
