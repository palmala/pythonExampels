import uvicorn
from fastapi import FastAPI
from architecture_testing.app.presentation import presentation

app = FastAPI()


@app.get(path="/")
async def root():
    return presentation.Presentation.get_json()


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
