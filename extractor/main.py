import os, sys, signal
import asyncio
import nats
from extractor.queue import Queue
from extractor.content_processor import ContentProcessor


def show_usage():
    usage = """
nats-pub [-s SERVER] <subject>

Example:

nats-sub -s demo.nats.io help -q workers 
"""
    print(usage)


def show_usage_and_die():
    show_usage()
    sys.exit(1)


async def error_cb(e):
    print("Error:", e)


async def closed_cb():
    # Wait for tasks to stop otherwise get a warning.
    await asyncio.sleep(0.2)
    loop.stop()


async def reconnected_cb():
    print("Got reconnected to NATS...")


async def subscribe_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print(
        "Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data
        )
    )


async def run():
    subject = 'contextual-engine-extractor'
    options = {
        "error_cb": error_cb,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb,
        'servers': os.getenv("NATS_URI")
    }

    nc = None
    try:
        nc = await nats.connect(**options)
    except Exception as e:
        print(e)
        show_usage_and_die()

    print(f"Listening on [{subject}]")

    def signal_handler():
        if nc.is_closed:
            return
        asyncio.create_task(nc.drain())

    for sig in ('SIGINT', 'SIGTERM'):
        asyncio.get_running_loop().add_signal_handler(getattr(signal, sig), signal_handler)

    content_processor = ContentProcessor()
    q = Queue(nc, subject, content_processor)
    await q.subscribe()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    try:
        loop.run_forever()
    finally:
        loop.close()

