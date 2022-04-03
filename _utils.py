from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import asyncio
import functools
from typing import Union
from pyrogram.types import Message

max_workers = multiprocessing.cpu_count() * 5
exc_ = ThreadPoolExecutor(max_workers=max_workers)

def run_in_exc(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(exc_, lambda: f(*args, **kwargs))
    return wrapper


def get_text(message: Message) -> Union[None, str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None