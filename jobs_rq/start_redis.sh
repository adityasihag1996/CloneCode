#!/bin/bash

# Check if Redis is installed
if ! command -v redis-server >/dev/null 2>&1; then
    echo "Redis is not installed. Installing Redis..."
    # Update package lists
    sudo apt-get update
    # Install Redis
    sudo apt-get install redis-server -y
else
    echo "Redis is already installed."
fi

# Configure Redis to start on a specific port
REDIS_PORT=6379  # Replace 6379 with your desired port

# Modify Redis configuration to use the specified port
if [ -f /etc/redis/redis.conf ]; then
    sudo sed -i "s/^port .*/port $REDIS_PORT/" /etc/redis/redis.conf
else
    echo "Redis configuration file not found."
    exit 1
fi

# Start Redis server
echo "Starting Redis server on port $REDIS_PORT..."

if command -v service >/dev/null 2>&1; then
    sudo service redis-server restart
elif command -v systemctl >/dev/null 2>&1; then
    sudo systemctl restart redis-server
else
    echo "Service management tool not found. Cannot restart Redis server."
    exit 1
fi

echo "Redis server is running on port $REDIS_PORT."

