import asyncio

# Import your classes
from src.components.app import App
from prometheus_client import start_http_server


async def main():
    # 1. Define the URL (usually loaded from an environment variable like os.getenv("REDIS_URL"))
    # If running locally:
    # make the app
    app = App(mock=True)
    metrics_port = 8000
    start_http_server(metrics_port, addr="0.0.0.0")
    try:
        
        
        # 6. Start the infinite worker loop
        await app.run()
        
    finally:
        # ALWAYS close the connection pool when the app shuts down
        await app.task_bus_infras.redis_client.close()

if __name__ == "__main__":
    asyncio.run(main())