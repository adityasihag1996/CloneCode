import signal
from functools import wraps

# Define the timeout exception
class TimeoutError(Exception):
    pass

# Define the signal handler
def timeout_handler(signum, frame):
    raise TimeoutError

# Define the decorator
def timeout(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Set the signal handler and a alarm
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                # Cancel the alarm after function
                signal.alarm(0)
            return result
        return wrapper
    return decorator