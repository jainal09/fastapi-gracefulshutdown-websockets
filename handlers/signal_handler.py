# Define the signal handler function
import asyncio
import sys as system

from uvicorn.server import HANDLED_SIGNALS

from services.db_ops.flag_ops import create_or_update_flag
from settings import settings_config

queue = settings_config.queue
server = settings_config.server
manager = settings_config.manager


class SignalHandler:

    async def handle_exit(self, loop:asyncio.AbstractEventLoop):
        print("Signal intercepted")
        create_or_update_flag(False)
        while len(queue) > 0:
            print("Waiting for the queue to be consumed")
            await asyncio.sleep(5)
        print("Queue is empty. Exiting.")
        await manager.close_all_connections()
        await manager.wait_for_connections_to_close()
        await server.shutdown()
        await server.lifespan.shutdown()
        for task in asyncio.all_tasks():
            try:
                task.cancel()
            except asyncio.CancelledError:
                pass
        try:
            await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
        except asyncio.CancelledError:
            pass
    
    def signal_handler(self, signame, sig, loop):
        asyncio.create_task(self.handle_exit(loop))

    def register_signal_handler(self):
        loop = asyncio.get_running_loop()
        signal_handlers = getattr(loop, "_signal_handlers", {})
        for sig in HANDLED_SIGNALS:
            loop.add_signal_handler(sig, self.signal_handler, sig, None, loop)