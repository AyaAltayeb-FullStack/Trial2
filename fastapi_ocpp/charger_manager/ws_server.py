import asyncio
import websockets
from charger_manager.handlers import ChargePointHandler

connected_chargers = {}  # charger_id: ChargePointHandler instance

async def on_connect(websocket, path):
    charger_id = path.strip("/")
    cp_handler = ChargePointHandler(charger_id, websocket)
    connected_chargers[charger_id] = cp_handler
    try:
        await cp_handler.start()
    except websockets.exceptions.ConnectionClosedOK:
        print(f"🔌 Charger {charger_id} disconnected.")
    except Exception as e:
        print(f"❌ Error for {charger_id}: {e}")

async def start_websocket_server():
    print("🚀 WebSocket server starting on ws://0.0.0.0:9000")
    server = await websockets.serve(on_connect, "0.0.0.0", 9000)
    await server.wait_closed()
