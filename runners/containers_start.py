import docker
from io import BytesIO

client = docker.from_env()
num_containers = 4 # Number of logical CPUs

image_name = "runner_worker"
# docker build -t runner_worker .

containers = []
for i in range(num_containers):
    container = client.containers.run(
        image_name,
        detach = True,
        read_only = True,  # Mounts the container's root filesystem as read only
        pids_limit = 10,  # Limits the number of concurrent processes
        mem_limit = '256m',  # Limits the memory usage
        cpuset_cpus = str(i)  # Assigns the container to a specific CPU
    )
    print(f"Launched secure container: {container.id}")
    containers.append(container)
    