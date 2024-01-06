from redis import Redis
from rq import Worker, Queue, Connection
from multiprocessing import Process

from DockerManager import DockerManager

def start_worker():
    # RQ conn
    redis_rq_conn = Redis(host = 'localhost', port = 4567, db = 0)   # host = '192.168.1.6'
    redis_rq = Queue('runs', connection = redis_rq_conn)

    with Connection(redis_rq_conn):
        worker = Worker([redis_rq])
        worker.work()

if __name__ == '__main__':
    parallels = 1

    # local Redis conn
    local_redis = Redis(
        host = 'localhost',
        port = 8899,
        db = 0,
        decode_responses = True,
    )

    docker_manager = DockerManager()
    # docker_manager.destroyAllContainers()

    # create containers
    docker_containers = docker_manager.createContainers(num_containers = parallels)

    # store the container ids in local redis
    for container in docker_containers:
        # local_redis.getset(f"{container.id}", "false")
        local_redis.zadd('containers', {container.id: 0})  # Mark as free
        
    # create and start worker processes
    processes = []
    for _ in range(parallels):
        process = Process(target=start_worker)
        process.start()
        processes.append(process)

    # join the processes
    for process in processes:
        process.join()

    
