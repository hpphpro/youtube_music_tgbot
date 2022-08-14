import asyncio
import sys

from utils.logger import info


def connection_retry(func):
    '''A simple decorator 
    handle errors that may appear due to the abundance of requests or incorrect data
    If error appear -> tries to retry request 5 times with 2 seconds delay
    '''
    async def wrap(*args, **kwargs):
        retries = 1
        while retries < 6:
            try:
                result = await func(*args, **kwargs)
            except Exception as ex:
                info(f'Got unexpected error {ex}\n\
                    Retrying to connect...{retries}')
                retries += 1
                await asyncio.sleep(2)
            else:
                return result
        raise Exception('Maximum connections retries exceeded')
    return wrap

def event_loop(f):
    '''A decorator that checks on existing event loop and starts it, otherwise doing nothing'''
    def decorator(*args, **kwargs):
        try:
            asyncio.get_running_loop()
        except RuntimeError: 
            return asyncio.run(f(*args, **kwargs))
        
        return f(*args, **kwargs)
    
    return decorator