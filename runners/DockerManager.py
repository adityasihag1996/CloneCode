import docker

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()

    def createContainers(self, num_containers = 4, image_name = "runner_worker"):
        containers = []
        for i in range(num_containers):
            container = self.client.containers.run(
                image_name,
                detach = True,
                read_only = True,  # Mounts the container's root filesystem as read only
                network_disabled = True,  # Disables networking
                pids_limit = 10,  # Limits the number of concurrent processes
                mem_limit = '256m',  # Limits the memory usage
                cpuset_cpus = str(i),  # Assigns the container to a specific CPU
            )
            print(f"Launched secure container: {container.id}")
            containers.append(container)

        return containers
    
    def destroyAllContainers(self):
        containers = self.client.containers.list(all=True)

        # Stop and remove each container
        for container in containers:
            print(f"Stopping container {container.id}...")
            container.stop()
            print(f"Removing container {container.id}...")
            container.remove()

        print("All containers have been stopped and removed.")

