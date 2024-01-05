import docker
from io import BytesIO

client = docker.from_env()
num_containers = 4 # Number of logical CPUs

image_name = "runner_worker"
# docker build -t runner_worker .

containers = []
for _ in range(num_containers):
    container = client.containers.run(
        image_name,
        # command=["sleep", "infinity"],  # Keeps the container alive
        detach=True,
        read_only=True,  # Mounts the container's root filesystem as read only
        # network_disabled=True,  # Disables networking
        pids_limit=10,  # Limits the number of concurrent processes
        mem_limit='256m',  # Limits the memory usage
    )
    print(f"Launched secure container: {container.id}")
    containers.append(container)
    