# https://hub.docker.com/r/ollama/ollama
# https://github.com/ollama/ollama
# bash ./LLM/DockerOllama.sh
# sh ./LLM/DockerOllama.sh

#!/bin/bash

if [ $(docker ps -a -q -f name=ollama) ]; then
    echo "Container ollama already exists."
    echo "Starting ollama..."
    docker start ollama
else
    echo "Pulling docker image ollama/ollama..."
    # Pull the Ollama Docker image
    docker pull ollama/ollama
    echo "Running ollama"
    # Run the Ollama container
    docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
fi

sleep 10

# Download/ Run the ollama model
# docker exec -it ollama ollama run llama3
docker exec ollama ollama run llama3

# Prompt 1: I will give you some product descriptions. Help me to optimise these descriptions.
# Subsequent prompts - Input product descriptions and the model will return the optimised product descriptions.