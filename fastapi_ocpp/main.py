import asyncio
import uvicorn
from fastapi import FastAPI
from charger_manager.ws_server import start_websocket_server

app = FastAPI(title="OCPP FastAPI Server")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_websocket_server())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
