#!/bin/bash

# Script paths
script0="/home/rohit/news/website/pages/youtube.py"
script1="/home/rohit/news/website/pages/top5.py"
script2="/home/rohit/news/website/pages/cluster.py"
script3="/home/rohit/news/website/pages/tagger.py"
script4="/home/rohit/news/website/pages/final.py"
script5="/home/rohit/news/website/pages/feedcron.py"

# Function to execute a script with retry logic
execute_script() {
    local script_path=$1
    local max_retries=4
    local retry_count=0
    local timeout=120

    echo "Executing script: $script_path"
    python3 "$script_path" --timeout $timeout

    if [ $? -eq 0 ]; then
        echo "Script executed successfully: $script_path"
    else
        echo "Script failed: $script_path"
    fi
}

# Execute scripts in priority order
# Execute scripts in priority order
execute_script "$script0"
sleep 1800 # Wait for 30 minutes

execute_script "$script1"
sleep 1800 # Wait for 30 minutes

execute_script "$script2"
sleep 1800 # Wait for 30 minutes

execute_script "$script3"
sleep 1800 # Wait for 30 minutes

execute_script "$script4"
sleep 1800 # Wait for 30 minutes

execute_script "$script5"
# No need to sleep after the last script