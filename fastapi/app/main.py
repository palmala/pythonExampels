#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def read_main():
	return {"msg": "Hello-bello"}

if __name__ == '__main__':
	uvicorn.run(app)