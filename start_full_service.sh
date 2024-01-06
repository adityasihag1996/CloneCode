#!/bin/bash

# Function to start a new tmux session and initialize Conda environment
start_tmux_session_with_conda_command() {
    local session_name=$1
    local conda_env=$2
    local python_version=$3
    local commands=$4

    tmux new-session -d -s "$session_name"
    tmux send-keys -t "$session_name" "source $(conda info --base)/etc/profile.d/conda.sh" C-m
    tmux send-keys -t "$session_name" "conda create -y -n $conda_env python=$python_version" C-m
    tmux send-keys -t "$session_name" "conda activate $conda_env" C-m
    tmux send-keys -t "$session_name" "$commands" C-m
    tmux detach-client -s "$session_name"
}

# Function to grant execute permissions to a script
grant_execute_permissions() {
    chmod +x "$1/start_redis.sh"
}

# Grant execute permissions to the start_redis.sh scripts
grant_execute_permissions jobs_rq
grant_execute_permissions metadata_db
grant_execute_permissions questions_db
grant_execute_permissions runners

# Function to start a new tmux session
start_tmux_session_with_command() {
    local session_name=$1
    local commands=$2

    tmux new-session -d -s "$session_name"
    tmux send-keys -t "$session_name" "$commands" C-m
    tmux detach-client -s "$session_name"
}

# 1. Execute start_redis.sh in /jobs_rq
start_tmux_session_with_command jrq "cd jobs_rq && ./start_redis.sh"

# 2. Execute start_redis.sh in /metadata_db
start_tmux_session_with_command mdb "cd metadata_db && ./start_redis.sh"

# 3. Execute start_redis.sh in /questions_db
start_tmux_session_with_command qdb "cd questions_db && ./start_redis.sh"

# 4. Start Flask server in /application with Conda environment 'app'
start_tmux_session_with_conda_command flask_server app 3.10 "cd application && pip install -r requirements.txt && python app.py"

# 5. Start Redis Docker and runner.py in /runners with Conda environment 'worker'
start_tmux_session_with_command redis_worker "cd runners && ./start_redis.sh"
start_tmux_session_with_conda_command worker worker 3.10 "cd runners && pip install -r requirements.txt && ./start_docker.sh && python runner.py"
