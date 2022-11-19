import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get(path="/", name="Home")
async def root():
    return templates.TemplateResponse("example.html", {"request": request, "buttons": buttons})


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
