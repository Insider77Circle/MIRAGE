import asyncio
import functools
import logging
from aiohttp import web

# --- Core Logic ---
from mirage_core import (
    Fabricator, MirageAI, handle_client,
    ACTIVE_PORTS
)

# --- Global State for Web Server ---
WEBSOCKETS = set()
# This will hold the latest system status to send to new clients
SYSTEM_STATUS = {"cpu": 12, "mem": 45, "threat": "LOW"}

# --- WebSocket Broadcaster ---
async def broadcast(message):
    """Sends a JSON message to all connected WebSocket clients."""
    if WEBSOCKETS:
        await asyncio.gather(*[ws.send_json(message) for ws in WEBSOCKETS])

async def web_event_handler(event):
    """
    Receives events from the core logic and decides what to do.
    For the web server, it broadcasts them to the UI.
    """
    # Update server-side state for future connections
    event_type = event.get("type")
    if event_type == "status_update":
        SYSTEM_STATUS["cpu"] = min(99, max(10, SYSTEM_STATUS["cpu"] + event["cpu_delta"]))
        SYSTEM_STATUS["mem"] = min(99, max(10, SYSTEM_STATUS["mem"] + event.get("mem_delta", 0)))
        # Send a consolidated status update
        await broadcast({"type": "status", "cpu": SYSTEM_STATUS["cpu"], "mem": SYSTEM_STATUS["mem"], "threat": SYSTEM_STATUS["threat"]})
    elif event_type == "threat_update":
        SYSTEM_STATUS["threat"] = event["level"]
        await broadcast({"type": "status", "cpu": SYSTEM_STATUS["cpu"], "mem": SYSTEM_STATUS["mem"], "threat": SYSTEM_STATUS["threat"]})
    else:
        # For other events (logs, connections), just forward them
        await broadcast(event)

# --- aiohttp Handlers ---
async def http_handler(request):
    """Serves the main index.html file."""
    return web.FileResponse('./mirage-v3-cyberpunk/index.html')

async def websocket_handler(request):
    """Handles WebSocket connections."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    WEBSOCKETS.add(ws)
    
    logging.info(f"WebSocket client connected: {request.remote}")
    # Send the current state to the newly connected client
    await ws.send_json({"type": "status", "cpu": SYSTEM_STATUS["cpu"], "mem": SYSTEM_STATUS["mem"], "threat": SYSTEM_STATUS["threat"]})
    await ws.send_json({"type": "ai_log", "message": "Backend connection established. Stand by for events..."})

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # We can implement client->server commands here in the future
                if msg.data == 'close':
                    await ws.close()
            elif msg.type == web.WSMsgType.ERROR:
                logging.error(f'WebSocket closed with exception {ws.exception()}')
    finally:
        WEBSOCKETS.remove(ws)
        logging.info(f"WebSocket client disconnected: {request.remote}")
        
    return ws

# --- Main Application Setup ---
async def main():
    # Use a lambda to create an async task for the event handler
    logger = lambda event: asyncio.create_task(web_event_handler(event))
    
    # 1. Initialize Core Components
    logging.info("Initializing asset generation...")
    fab = Fabricator(logger=logger)
    fab.run()
    
    logging.info("Initializing AI Kernel...")
    ai_engine = MirageAI(logger=logger)

    # 2. Start Honeypot Listeners
    honeypot_servers = []
    logging.info(f"Starting honeypot listeners on ports: {ACTIVE_PORTS}")
    for port in ACTIVE_PORTS:
        try:
            handler = functools.partial(handle_client, ai_engine=ai_engine, event_callback=web_event_handler)
            server = await asyncio.start_server(handler, '0.0.0.0', port)
            honeypot_servers.append(server)
        except PermissionError:
            logging.critical(f"PERMISSION ERROR: Failed to bind to port {port}. Try running with sudo/admin privileges.")
        except Exception as e:
            logging.critical(f"Failed to start listener on port {port}: {e}")

    if not honeypot_servers:
        logging.error("No honeypot listeners started. The application may not function as expected.")

    # 3. Setup and Run Web Server
    app = web.Application()
    app.router.add_get('/', http_handler)
    app.router.add_get('/ws', websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    # Use a different port for the web UI to avoid conflicts with the honeypot
    site = web.TCPSite(runner, '0.0.0.0', 8081) 
    await site.start()
    logging.info("="*50)
    logging.info("Mirage V3 Web Interface is running.")
    logging.info(f"Access the UI at: http://localhost:8081")
    logging.info("="*50)

    # Keep the application running indefinitely
    await asyncio.Event().wait()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Shutting down server...")

