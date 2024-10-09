# https://hub.docker.com/r/ollama/ollama
# https://github.com/ollama/ollama
# bash ./LLM/DockerOllama.sh

#!/bin/bash

# Pull the Ollama Docker image
docker pull ollama/ollama

# Run the Ollama container
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Wait for a moment to ensure the container starts
sleep 10

# Execute the command to run the llama model
docker exec -it ollama ollama run llama3

# OR if you already have created the container
# docker start ollama
# docker stop ollama

# Prompt 1: I will give you some product descriptions. Help me to optimise these descriptions.
# Subsequent prompts - Input product descriptions and the model will return the optimised product descriptions.
