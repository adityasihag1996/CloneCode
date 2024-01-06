# Check if Docker is installed
if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is not installed. Installing Docker..."
    # Install Docker using Homebrew
    brew install --cask docker
    # Open Docker to complete the installation and start the service
    open -a Docker
else
    echo "Docker is already installed."
fi

# Wait for Docker service to start
echo "Starting Docker service..."
while ! docker system info >/dev/null 2>&1; do
    echo "Waiting for Docker to start..."
    sleep 5
done

echo "Docker service is running."
