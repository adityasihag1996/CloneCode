from redis import Redis
from rq import Worker, Queue, Connection

# Connect to Redis server
redis_conn = Redis(
    host = '192.168.1.6',
    port = 4567,
    db = 0,
    password = 'yourpassword'
)

# Setup the queue and worker
redis_rq = Queue('runs', connection = redis_conn)

def start_worker():
    with Connection(redis_conn):
        worker = Worker([redis_rq])
        worker.work()

# Execute worker
if __name__ == '__main__':
    start_worker()

