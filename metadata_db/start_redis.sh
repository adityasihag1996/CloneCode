#!/bin/bash

# Check if Redis is installed
if ! command -v redis-server >/dev/null 2>&1; then
    echo "Redis is not installed. Installing Redis..."
    # Install Homebrew if not installed
    if ! command -v brew >/dev/null 2>&1; then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    # Install Redis using Homebrew
    brew install redis
else
    echo "Redis is already installed."
fi

# Specify the desired port for Redis
REDIS_PORT=6789

# Start Redis server on the specified port
echo "Starting Redis server on port $REDIS_PORT..."
redis-server --port $REDIS_PORT

echo "Redis server is running on port $REDIS_PORT."
