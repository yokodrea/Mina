#!/bin/bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull your model
ollama pull phi  # or tinyllama

# Start Ollama in background
nohup ollama serve > /tmp/ollama.log 2>&1 &


# ./setup.sh dn't forget to run this after reset andthen start project
