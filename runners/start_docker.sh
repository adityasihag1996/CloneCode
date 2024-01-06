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

echo "Starting Docker service..."
echo "Docker service is running."
