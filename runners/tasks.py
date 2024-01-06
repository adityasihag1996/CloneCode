import time
import docker
from redis import Redis

def process_data(json_data):
    local_redis = Redis(
        host = 'localhost',
        port = 8899,
        db = 0,
        # password = 'yourpassword',
        decode_responses = True,
    )

    free_containers = local_redis.zrangebyscore('containers', min=0, max=0, start=0, num=1)
    container = docker.from_env().containers.get(str(free_containers[0]))
    local_redis.zadd('containers', {container.id: 1})  # Mark as busy

    ## DO SOME PROCESSSING IN THE CONTAINER
    exec_log = container.exec_run(f"python -c '{json_data['code']}'", workdir = "/app")
    print(f"Container {container.id} output:")
    print(exec_log.output.decode())

    local_redis.zadd('containers', {container.id: 0})  # Reset to free

# def process_data(json_data):
#     all_containers = docker.from_env().containers.list()
#     local_redis = Redis(
#         host = 'localhost',
#         port = 8899,
#         db = 0,
#         # password = 'yourpassword',
#         decode_responses = True,
#     )

#     # choose a free container
#     for container in all_containers:
#         key = f"{container.id}"
#         if local_redis.getset(key, "true") == "false":
#             break

#     ## DO SOME PROCESSSING IN THE CONTAINER
#     exec_log = container.exec_run(f"python -c '{json_data['code']}'", workdir = "/app")
#     print(f"Container {container.id} output:")
#     print(exec_log.output.decode())

#     local_redis.getset(key, "false")